package main.alscala

import org.apache.log4j.{Level, Logger}
import org.apache.spark.mllib.recommendation.{ALS, Rating}
import org.apache.spark.{SparkConf, SparkContext}


/**
  * 本地模式运行
  */
object alsforcompany{
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local[*]").setAppName("als recommendation fro company")
    val sc = new SparkContext(conf)
    Logger.getRootLogger.setLevel(Level.ERROR)
    sc.setLogLevel("ERROR")
    // 1. 加载并解析数据
    val data = sc.textFile("/home/cgt/sparkcompetion/investment-spark/src/main/resources/socrereal.txt")
    val ratings = data.map(_.split(",") match { case Array(company, investagency, rate) =>
      Rating(company.toInt, investagency.toInt, rate.toDouble)
    }).cache()

    val company = ratings.map(_.user).distinct()
    val investagency = ratings.map(_.product).distinct()
    println("Got "+ratings.count()+" ratings from "+company.count+" companies on "+investagency.count+" investagencies.")


    // 2. 训练als模型
    val rank = 6
    val lambda = 0.01
    val numIterations = 5
    val model = ALS.train(ratings, rank, numIterations, lambda)

    // 3. 计算均方差
    //从 ratings 中获得只包含公司和投资机构的数据集
    val companyAgency = ratings.map { case Rating(user, product, rate) =>
      (user, product)
    }
    //使用推荐模型对投资机构进行预测评分，得到预测评分的数据集
    val predictions = model.predict(companyAgency).map { case Rating(user, product, rate) =>
      ((user, product), rate)
    }

    //将真实评分数据集与预测评分数据集进行合并
    val ratesAndPreds = ratings.map { case Rating(user, product, rate) =>
      ((user, product), rate)
    }.join(predictions)

    //计算评估系数rmse越小推荐效果越好
    val rmse= math.sqrt(ratesAndPreds.map { case ((company, companyAgency), (r1, r2)) =>
      val err = (r1 - r2)
      err * err
    }.mean())

    println(s"RMSE = $rmse")

    //4.对所有融资公司进行推荐,并保存推荐结果
    val allRecs = model.recommendProductsForUsers(10).map{case (companyId,preArray)=>
      var productpre =""
      for(i <- 0 until 10){
        if(i !=9)
          productpre += companyId+","+preArray(i).product+","+preArray(i).rating+"\n"
        else
          productpre += companyId+","+preArray(i).product+","+preArray(i).rating

      }
      (companyId, productpre)
    }
    //并保存推荐结果
    val allpre = allRecs.sortBy(_._1).map{
      case (companyId,productpre) => productpre
    }.repartition(1).saveAsTextFile("/home/cgt/sparkcompetion/als/predict")

  }
}
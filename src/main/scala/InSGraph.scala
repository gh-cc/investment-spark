package vs

import org.apache.log4j.{Level, Logger}
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark._
import org.apache.spark.graphx._

import scala.collection.mutable.ArrayBuffer

/**
  * Created by GH-GAN on 2016/7/19.
  */
object InSGraph {
  def main(args: Array[String]) {
    Logger.getRootLogger.setLevel(Level.ERROR)
    val conf = new SparkConf().setMaster("local[*]").setAppName("ins")
    val sc = new SparkContext(conf)
    sc.setLogLevel("ERROR")
    //    val data: RDD[String] = sc.textFile("D:\\workspace\\investment-spark\\src\\main\\resources\\itjuzi_new_firms.txt")
    val event_data = sc.textFile("D:\\workspace\\investment-spark\\src\\main\\resources\\itjuzi_events_total.txt")
      .filter(!_.trim.startsWith("#")).map(_.split(",")).filter(_.length == 8)

    // (融资公司，投资公司)
    val ed = event_data.map(line => (line(1).trim,line(6).trim)).flatMap(line => {
      val tzgs: Array[String] = line._2.split(" +")
      var arr = new ArrayBuffer[(String,String)]()
      if(tzgs.size > 1){
        for(i <- 0 to tzgs.size - 1){
          if(!"".eq(tzgs(i).trim)){
            arr.+=((line._1,tzgs(i).trim))
          }
        }
      }
      arr
    })

    // 所有融资公司及投资公司 => 点
    val vd: RDD[String] = ed.flatMap(line => Array(line._1,line._2)).distinct()

    val _vd = vd.map(name => (Tool.get(name).toLong,(name,0,0)))   // (id,(name,出度，入度))
    val _ed = ed.map(e => Edge(Tool.get(e._2),Tool.get(e._1),""))  // 投资，融资
    val graph = Graph(_vd,_ed)


    // 投资公司角度
    val tz_outDegrees = graph.outDegrees.sortBy(-_._2)
    val tz_inDegrees = graph.inDegrees.sortBy(-_._2)
    val max_out = tz_outDegrees.take(1).apply(0)._2.toDouble
    val out_map = tz_outDegrees.collect().toMap
    val in_map = tz_inDegrees.collect().toMap


    val new_graph = graph.mapVertices((VertexId, VD) => {
     if(VD!=null){
       var out = 0
       var in = 0
       if(out_map.contains(VertexId)){  try{ out = out_map.get(VertexId).get }catch {case ex:Exception => out = 0}}
       if(in_map.contains(VertexId)){ try{ in = in_map.get(VertexId).get }catch {case ex:Exception => in = 0} }
       (VD._1,out,in)
     }
    })

    //所有点
    /*
    Tool.saveToFile(
      new_graph.map(line => {
        "{\"color\": \"" + Tool.getColor + "\", \"label\": \""+ line._2._1 +"\", \"attributes\": {}, \"y\": "+Tool.getXY()+", \"x\": "+Tool.getXY()+", \"id\": \""+line._1+"\", \"size\": "+(line._2._2.toDouble / max_out * 120 + 10).toInt+"},"
      }).collect(),
      "D:\\workspace\\investment-spark\\src\\main\\resources\\vd.txt"
    )*/

    //所有边
   /* Tool.saveToFile(
      graph.edges.map(e => {
        "{\"sourceID\": \""+e.srcId+"\", \"attributes\": {}, \"targetID\": \""+e.dstId+"\", \"size\": 1},"
      }).collect(),
      "D:\\workspace\\investment-spark\\src\\main\\resources\\ed.txt"
    )*/

    //投资前top5的投资公司及关联的所有融资公司
    val top5 = sc.parallelize(tz_outDegrees.take(5)).join(new_graph.edges.map(e => (e.srcId,e.dstId)))
    Tool.saveToFile(
      top5.flatMap(vd => {
        Array((vd._1,vd._2._1),(vd._2._2,0))
      }).distinct().map(vd => {
        "{\"color\": \"" + Tool.getColor + "\", \"label\": \""+ Tool.IdToName(vd._1) +"\", \"attributes\": {}, \"y\": "+Tool.getY()+", \"x\": "+Tool.getX()+", \"id\": \""+vd._1+"\", \"size\": "+(vd._2.toDouble / max_out * 90 + 10).toInt+"},"
      }).collect(),
      "D:\\workspace\\investment-spark\\src\\main\\resources\\tz-top5_vd.txt"
    )
    //投资前top10的投资公司及关联的所有融资公司边
    Tool.saveToFile(
      top5.map(ed => {
        "{\"sourceID\": \""+ed._1+"\", \"attributes\": {}, \"targetID\": \""+ed._2._2+"\", \"size\": 1},"
      }).collect(),
      "D:\\workspace\\investment-spark\\src\\main\\resources\\tz-top5_ed.txt"
    )

    //融资前top5的融资公司及关联的所有投资公司
    val rz_top5 = sc.parallelize(tz_inDegrees.take(5)).join(new_graph.edges.map(e => (e.dstId,e.srcId)))
    Tool.saveToFile(
      rz_top5.flatMap(vd => {
        Array((vd._1,vd._2._1),(vd._2._2,0))
      }).distinct().map(vd => {
        "{\"color\": \"" + Tool.getColor + "\", \"label\": \""+ Tool.IdToName(vd._1) +"\", \"attributes\": {}, \"y\": "+Tool.getY()+", \"x\": "+Tool.getX()+", \"id\": \""+vd._1+"\", \"size\": "+(vd._2.toDouble / max_out * 90 + 10).toInt+"},"
      }).collect(),
      "D:\\workspace\\investment-spark\\src\\main\\resources\\rz-top5_vd.txt"
    )
    Tool.saveToFile(
      rz_top5.map(ed => {
        "{\"sourceID\": \""+ed._1+"\", \"attributes\": {}, \"targetID\": \""+ed._2._2+"\", \"size\": 1},"
      }).collect(),
      "D:\\workspace\\investment-spark\\src\\main\\resources\\rz-top5_ed.txt"
    )

  }
}

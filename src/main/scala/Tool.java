package vs;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.util.*;

/**
 * Created by GH-GAN on 2016/7/12.
 */
public class Tool {
    public static Long num = 0L;
    public static HashMap<String,Long> map = new HashMap<String,Long>();
//    private static HashMap<Long,String> id = new HashMap<Long,String>();
    public static Long get(String key){
        if (map.containsKey(key)){
            return map.get(key);
        }else{
            num = num + 1;
            map.put(key,num);
            return num;
        }
    }
    public static String IdToName(Long lon){
        for(Map.Entry<String, Long> entries : map.entrySet()){
            if(entries.getValue().equals(lon)){
                return entries.getKey();
            }
        }
        return "";
    }
    private static ArrayList<String> color = new ArrayList<String>();
    static {
        color.add("#00FF00"); color.add("#00FFFF");
        color.add("#000066"); color.add("#0000FF");
        color.add("#33CCCC"); color.add("#336600");
        color.add("#660000"); color.add("#669900");
        color.add("#993300"); color.add("#9933FF");
        color.add("#993399"); color.add("#CC3300");
        color.add("#CC0099"); color.add("#CCCC00");
        color.add("#CCFF00"); color.add("#CC66FF");
        color.add("#FF0000"); color.add("#FF3366");
        color.add("#FF00FF"); color.add("#FFFF00");
        color.add("#FFFFCC"); color.add("#FFCC66");
    }
    private static Random random = new Random();
    public static String getColor(){
        return color.get(random.nextInt(color.size()));
    }
    public static int getX(){
        return random.nextInt(850)-100;
    }
    public static int getY(){
        return random.nextInt(300)-200;
    }
    public static void saveToFile(String [] arr,String file){
        try {
            FileOutputStream out = new FileOutputStream(file);
            BufferedWriter bufw = new BufferedWriter(new OutputStreamWriter(out,"UTF-8"));
            for (String s : arr){
                bufw.write(s);
                bufw.newLine();
                bufw.flush();
            }
            bufw.close();
            out.close();
        }catch (Exception e){
            System.out.println(e);
        }

    }
}

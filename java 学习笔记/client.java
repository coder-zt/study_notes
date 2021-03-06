import java.util.HashMap;
import java.util.Map;

public class client{

        public static int romanToInt(String s) {
            Map<Character, Integer> toInt = new HashMap<Character, Integer>();
            toInt.put('I', 1);
            toInt.put('V', 5);
            toInt.put('X', 10);
            toInt.put('L', 50);
            toInt.put('C', 100);
            toInt.put('D', 500);
            toInt.put('M', 1000);
            int currentNum;
            int num = 0;
            int temp = 0;
            for(int i=0;i<s.length();i++){
               currentNum = toInt.get(s.charAt(i));
               if(currentNum > temp){
                   num = num - 2*temp + currentNum;
               }else{
                   num += currentNum;
               }
               temp = currentNum;
            }
           
            return num;
        }

    public static void main(String[] args) {
        System.out.println("" + romanToInt("MCMXCIV"));
        // IUserInfo userInfo = new adapter();
        // System.out.println(userInfo.getName());
        // System.out.println(userInfo.getAddres());
        // System.out.println(userInfo.getPhone());
    }
}


//目标对象接口
interface IUserInfo{
    //获取员工名称
    String getName();
    //获取员工电话
    String getPhone();
    //获取员工家庭地址
    String getAddres();
}

//源对象接口
interface IOutUserInfo{
    //获取员工信息
    //@return {"name": "姓名"，"phone":"电话, "addres","地址"}
    Map getUserInfo();
}

//目标类的实现
class UserInfo{
    //获取员工名称
    String getName(){
        return "姓名";
    }
    //获取员工电话
    String getPhone(){
        return "电话";
    }
    //获取员工家庭地址
    String getAddres(){
        return "地址";
    }
}

//源类的实现
class OutUserInfo{
    Map getUserInfo(){
        Map userInfo = new HashMap();
        userInfo.put("name","姓名");
        userInfo.put("phone","电话");
        userInfo.put("adress","地址");
        return userInfo;
    }
}

//适配器->继承源类，实现目标类的接口
class adapter extends OutUserInfo implements IUserInfo{
    Map userInfo = super.getUserInfo();
    //获取员工名称
    public String getName(){
        return (String)super.getUserInfo().get("name");
    }
    //获取员工电话
    public String getPhone(){
        return (String)super.getUserInfo().get("phone");
    }
    //获取员工家庭地址
    public String getAddres(){
        return (String)super.getUserInfo().get("adress");
    }
}



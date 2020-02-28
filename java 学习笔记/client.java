import java.util.HashMap;
import java.util.Map;

public class client{
    public static void main(String[] args) {
        IUserInfo userInfo = new adapter();
        System.out.println(userInfo.getName());
        System.out.println(userInfo.getAddres());
        System.out.println(userInfo.getPhone());
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
        return (String)userInfo.get("name");
    }
    //获取员工电话
    public String getPhone(){
        return (String)userInfo.get("phone");
    }
    //获取员工家庭地址
    public String getAddres(){
        return (String)userInfo.get("adress");
    }
}



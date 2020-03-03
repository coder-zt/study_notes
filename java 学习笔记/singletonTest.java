class signleton {
    private signleton() {
    };

    private static signleton mSignleton = null;

    public static signleton getInstance() {
       
        if(mSignleton == null){
            mSignleton = new signleton();
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        return mSignleton;
    }

} 

public class signletonTest{

    public static void main(String[] args) {
        while(true){
        new Thread(new Runnable(){
        
            @Override
            public void run() {
                // TODO Auto-generated method stub
                System.out.println( signleton.getInstance().toString());
            }
        }).start();
    }
    }
}
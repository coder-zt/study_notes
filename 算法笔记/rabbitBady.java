public class rabbitBady{

    public static int getCount(int n){
        int count_out = 2;
        int count_grow_1 = 0;
        int count_grow_2 = 0;
        int temp = 0;
        for(int i=1;i<=n;i++){
            if(i>= 3){
                temp = count_grow_1;
                count_grow_1 = count_out;
                count_out += count_grow_2;
                count_grow_2 = temp;
            }
            System.out.println("out:" + count_out  + " 1:" + count_grow_1 + " 2:" + count_grow_2);
        }
        
        int data[] = {1,2,3};
        System.out.println( data.length + "");
        return count_out + count_grow_1 + count_grow_2;
       
    }

    static public int binSearch(int []array, int target){
        int low = 0, high = array.length - 1;
        int mid = 0;
        while(low < high){
                mid = (low + high)/2;
                if( array[mid] == target){
                    return mid;
                }
                else if(array[mid] > target){
                    high = mid - 1;
                }
                else if(array[mid] < target){
                    low = mid + 1;
                }
                   
        }
        if(array[high] == target){
            return high;
        }else{
            return high + 1;
        }
    }

    public static void main(String[] args) {
        int array[] = {1,2,3,4,5};
        int target = 6;
        System.out.println(binSearch(array, target));
    }

}
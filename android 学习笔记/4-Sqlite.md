# Sqlite数据库
## 创建数据库
1. 创建一个类继承于SQLiteOpenHelper
     1. @param context to use for locating paths to the the database
     2. @param name of the database file, or null for an in-memory database
     3. @param factory to use for creating cursor objects, or null for the default
     4. @param version number of the database (starting at 1); if the database is older,
2. 创建对象新建数据库
```java
    //创建数据库
    db_DatabaseHelper helper = new db_DatabaseHelper(this);
    helper.getWritableDatabase();
```
## onCreate(SQLiteDatabase db)
- 第一次创建数据库的时候调用该函数
    ```java
    //创建数据表(表名单独用类保存为常量)
    //1.编写sql语句
    String sql = "create table" + TABLE_NAME + "_id integer, name varhcar(50), age integer, salary integer";
    //2.执行sql语句
    db.execSQL(sql);
    ``` 

## onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion)
- 当数据库升级的时候调用该函数
- 根据版本号不同对数据库做相应的处理（增减字段等）
---
## 编写DAO操作类
1. 通过helper对象获取SQLiteDatabase对象
2. 编写sql语句
3. SQLiteDatabase对象执行sql语句
4. 关闭数据库
- eg:
    ```java
    QLiteDatabase db = mhelper.getWritableDatabase();
    String sql = "insert into " + db_Constants.TABLE_NAME + "(_id,name,age,salary,phone,address)values(?,?,?,?,?,?)";
    db.execSQL(sql, new Object[]{1,"张滔",21,3500,"13678088714","重庆开县"});
    db.close();
    ```
- 查询操作
     * 查询操作调用方法rawQuery(sql,null);
     * 该方法返回游标对象 Cursor
     * moveToNext()遍历返回结果
     * getColumnIndex("columnName");\\\通过列名获取列号
     * getString(index)\getInt(index);\\\通过列号获取数据
     * 关闭游标、数据库。
- eg:
    ```java
        SQLiteDatabase db = mhelper.getWritableDatabase();
        String sql = "select * from " + db_Constants.TABLE_NAME;
        Cursor cursor = db.rawQuery(sql,null);
        while(cursor.moveToNext()){
            int index = cursor.getColumnIndex("name");
            String name = cursor.getString(index);
            Log.d(TAG, name);
        }
        cursor.close();
        db.close();
    ```
---
## 使用Android API操作数据
- Android提供了数据操作的API，使操作数据库变得更加简单
- 插入
    * insert(数据表名称， null, ContentValues);
    * ContentValues是map容器，通过put()添加键值对及列名与其对应的值
    * @return (long)新插入的行号，若为-1表示发生错误
    * eg:
        ```java
        SQLiteDatabase db = mhelper.getWritableDatabase();
        //String sql = "insert into " + db_Constants.TABLE_NAME + "(_id,name,age,salary,phone,address)values(?,?,?,?,?,?)";
        //db.execSQL(sql, new Object[]{1,"张滔",21,3500,"13678088714","重庆开县"});
        ContentValues values = new ContentValues();
        values.put("_id", 1);
        values.put("name", "张滔");
        values.put("salary", 3500);
        values.put("phone", "13678088714");
        values.put("address", "重庆开县");
        db.insert(db_Constants.TABLE_NAME, null, values);
        db.close();
        ```
- 删除
    * delete(数据表名称, 条件, 参数)
    * 参数是用字符串数组表示，代替条件中的‘?’
    * @return (int)影响行数
    * eg:
        ```java
        SQLiteDatabase db = mhelper.getWritableDatabase();
        //String sql = "delete from " + db_Constants.TABLE_NAME + " where age = 30";
        //db.execSQL(sql);
        String[] Args = new String[1];
        Args[0] = "30";
        db.delete(db_Constants.TABLE_NAME,"age = ?",Args);
        db.close();
        ```
- 更新
    * update(数据表名称, ContentValues, 条件, 参数)
    * return (int)影响行数
    * eg:
        ```java
         SQLiteDatabase db = mhelper.getWritableDatabase();
        //String sql = "update " + db_Constants.TABLE_NAME + " set salary = 6500 where age =21";
        //db.execSQL(sql);
        ContentValues values = new ContentValues();
        values.put("salary", 6500);
        String[] Args = new String[1];
        Args[0] = "30";
        db.update(db_Constants.TABLE_NAME, values, "age = ?", Args);
        db.close();
        ```
- 查询
    * query(数据表名称, 返回字段, 条件, 参数, 分组, HAVING,排序)
    * HAVING 是条件中有函数的时候使用
    * @return (Cursor)游标
    ```java
     SQLiteDatabase db = mhelper.getWritableDatabase();
        // String sql = "select * from " + db_Constants.TABLE_NAME;
        // Cursor cursor = db.rawQuery(sql,null);
        // while(cursor.moveToNext()){
        //     int index = cursor.getColumnIndex("name");
        //     String name = cursor.getString(index);
        //     Log.d(TAG, name);
        // }
        // cursor.close();
        Cursor cursor = db.query(db_Constants.TABLE_NAME, null, null, null,null,null,null);
        while(cursor.moveToNext()){
            int index = cursor.getColumnIndex("name");
            String name = cursor.getString(index);
            Log.d(TAG, name);
        }
        db.close();
    ```
---
## 数据库事务
- 安全性
    * 当数据库在进行写操作时，由于异常发生，可能导致数据前后出现不一致的对象，因此有必要采用事务
        ```java
        db.beginTransaction();//开启事务
        try{//数据操作
            db.setTransactionSuccessful();
        }catch(exception e){
            //处理异常
        }finally{
            db.endTransaction();//关闭事务
            db.close();
        }
            
        ```
- 高效性
    * 在执行大量数据操作时，普通方式会重复打开关闭数据库，而开启事务后，是将数据先写入内存，再一次性写入数据。
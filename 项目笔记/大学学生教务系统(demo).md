# 大学学生教务系统模拟DEMO
## 系统角色
- 管理员
    * 填写专业信息 -> 专业信息表
        - profession(_id, name, teach_id)
    * 填写课程信息 -> 课程信息表
        - course(_id, name, credit, time, pro_id)
    * 填写教师职位 -> 补充教师信息表
        - position
    * 展示教师信息 -> select * from teach;
    * 展示学生信息 -> select * feom student;
- 学生
    * 注册 -> 学生信息表
        - student(_id, name, studnet_id, sex, phone, pro_id)
    * 选课 -> 选课表
        - stu_course(_id, stu_id, cou_id, grade)
    *  查询成绩单->select course.name, studenn.name from course, student where stu_coures.stu_id = ?;
- 教师
    * 注册 -> 教师信息表
        - teach(_id, name, position, pro_id)
    * 上传分数 -> 补充选课信息表
        - grade
---
## 数据库
- 名称：uaas(University Academic Affairs System)
- 数据表
    * 专业数据表
        - profession(_id, name, <u>teach_id</u>)
        ```sql
        create table profession(_id int,
                                name varchar(20),
                                teach_id int);
        ```

        - 操作
            * 插入
                - 新增专业->名称
            * 查询
                - 学生、老师注册选择专业->全部专业
                - 查询专业主任
            * 更新
                - 添加专业主任
            * 删除
                - 删除专业
    
    * course(_id, name, credit, time, <u>pro_id</u>)
    ```sql
    create table course(_id int,
                        name varchar(20),
                        credit varchar(2),
                        time varchar(10),
                        pro_id int);
    ```
    * student(_id, name, studnet_id, sex, phone, <u>pro_id</u>)
    ```sql
    create table student(_id int,
                        student_id varchar(20),
                        sex varchar(2),
                        phone varchar(11),
                        pro_id int);
    ```
    * teach(_id, name, position, <u>pro_id</u>)
    ```sql
    create table teacher(_id int,
                        name varchar(20),
                        position varchar(10),
                        pro_id int);
    ```
    * stu_course(_id, <u>stu_id, cou_id</u>, grade)
    ```sql
    create table stu_course(_id int,
                            stu_id int,
                            cou_id int,
                            grade int);
    ```
- 数据传递方式
    * 使用对象
---
## 1.登录页面
- UI
    * 利用单选框选择身份
    * 学/工号
    * 密码
    * 登录|注册
- 管理员
    * 登录-> 账号：admin，密码：123456
- 学生
    * 注册-> 姓名，性别， 电话，专业, 学号（根据数据库里的信息自动生成）， 密码（6位）
    * 登录->学号，密码
- 教师
    * 注册-> 姓名，专业, 工号（根据数据库里的信息自动生成）， 密码（6位）
    * 登录->工号，密码

## 2.管理员页面
- 添加专业-实现（2/5）
- 设置专业主任->等待教师注册信息后再设置
- 添加课程（2/6）
    * 名称
    * 学分
    * 老师 -->教师注册时选择自己教授课程
    * 开课时间
    * 所属专业）
    * 实现（名称，所属专业）多字段唯一
        - 创建唯一索引
        ```java
        String sql = "CREATE unique INDEX unique_info on " + db_constants.TABLE_COURSE +" (name, pro_id);";
        db.execSQL(sql);
        ```
- 展示所有数据表-实现（2/4）
    * 使用了PopupWindow展示了所有数据表->选择展示表格
## 3.教师注册页面
- 教师数据表====teach(_id, name, position,work_index, user_psd, id,pro_id)
- UI：姓名、职务、专业、登录密码、并自动返回工号(2/8)
## 4.教师页面
- 登录：根据工号和密码登录教师页面

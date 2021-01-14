## p1 navigation介绍
- navgation是jetPack中框架的一部分，其作用是帮助你更好的管理页面中的跳转

## p2 navigation基本使用

1. 添加依赖
```gradle
dependencies {
  def nav_version = "2.3.2"

  // Java language implementation
  implementation "androidx.navigation:navigation-fragment:$nav_version"
  implementation "androidx.navigation:navigation-ui:$nav_version"

  // Kotlin
  implementation "androidx.navigation:navigation-fragment-ktx:$nav_version"
  implementation "androidx.navigation:navigation-ui-ktx:$nav_version"

  // Feature module Support
  implementation "androidx.navigation:navigation-dynamic-features-fragment:$nav_version"

  // Testing Navigation
  androidTestImplementation "androidx.navigation:navigation-testing:$nav_version"

  // Jetpack Compose Integration
  implementation "androidx.navigation:navigation-compose:1.0.0-alpha04"
}
```

2. 使用fragment容器
```xml
 <androidx.fragment.app.FragmentContainerView
        android:id="@+id/nav_host_fragment"
        android:name="androidx.navigation.fragment.NavHostFragment"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        app:defaultNavHost="true"
        app:navGraph="@navigation/nav_graph" />
```

3. 创建navGraph

```xml
<?xml version="1.0" encoding="utf-8"?>

<!-- app:startDestination:最开始的目的地 -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    app:startDestination="@id/nav_login"
    android:id="@+id/nav_graph.xml">
    
    <fragment android:id="@+id/nav_login"
        android:name="com.Accountbook.fragment.LoginFragment"/>

    <fragment android:id="@+id/nav_register"
        android:name="com.Accountbook.fragment.RegisterFragment"/>

    <fragment android:id="@+id/nar_forget"
        android:name="com.Accountbook.fragment.ForgetFragment"/>

</navigation>
```

## p3 navigation实现页面跳转
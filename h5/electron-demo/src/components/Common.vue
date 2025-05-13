<template>
  <div class="contianer">
    <div
      class="flex flex-row justify-start space-x-3 items-start px-4 py-4 bg-white rounded-lg mt-4 mx-4"
    >
      <img
        src="../assets/ic_launcher.png"
        alt="app logo"
        class="w-12 h-12 rounded-lg"
      />
      <ul class="text-left">
        <li class="font-semibold text-xl">53伴学</li>
        <li class="text-gray-600 mt-2 text-ms w-96 flex">
          <span class="w-20 mr-2">应用包名</span>
          <span>com.diyiyin.online53</span>
        </li>
        <li class="text-gray-600 mt-1 text-ms w-96 flex">
          <span class="w-20 mr-2">当前版本</span>
          <span>3.00.03</span>
        </li>
        <li class="text-gray-600 mt-1 text-ms w-96 flex">
          <span class="w-20 mr-2">更新时间</span>
          <span>2025-03-13 16:28</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "CommonPage",
  props: {
    msg: String,
  },
};
</script>
<style scoped>
</style> 


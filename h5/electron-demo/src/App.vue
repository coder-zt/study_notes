<template>
  <div id="app" class="flex h-screen bg-">
    <div class="w-1/4 h-ful bg-purple-400">
      <img
        src="./assets/ic_launcher.png"
        alt="app logo"
        class="w-24 h-24 mx-auto mt-12 mb-2 border border-white rounded-lg"
      />
      <span class="text-black text-lg font-semibold">53伴学</span>
      <br />
      <span class="text-black text-lg font-semibold mt-2"
        >发布工具@1.0.0-beta</span
      >
    </div>

    <div class="w-3/4 h-full flex flex-col">
      <nav>
        <ul
          class="flex flex-row justify-between space-x-12 items-center py-3 px-2"
        >
          <li
            v-for="item in items"
            :key="item.id"
            :class="{
              'bg-purple-500 rounded-full': item.selected,
            }"
            class="w-full py-2 text-black text-lg font-semibold"
            @click="handleClick(item)"
          >
            {{ item.name }}
          </li>
        </ul>
      </nav>
      <router-view class="w-full h-full bg-gray-100"> </router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {
  },
  data() {
    return {
      items: [
        { name: "通用", selected: true, router: "/" },
        { name: "华为", selected: false, router: "/huawei" },
        { name: "Oppo", selected: false, router: "/oppo" },
        { name: "小米", selected: false, router: "/xiaomi" },
        { name: "Vivo", selected: false, router: "/vivo" },
      ],
    };
  },
  methods: {
    handleClick(item) {
      if(item.selected) return;
      this.items.forEach((i) => (i.selected = false));
      item.selected = true;
      this.$router.push(item.router);
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

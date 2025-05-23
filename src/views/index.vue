<template>
    <div class="wrapper">
      <!-- 侧边导航栏 -->
      <aside class="sidebar" :class="{ 'active': isSidebarOpen }">
        <div class="sidebar-header">
          <div style="display: flex;">
            <div><img style="width: 250px; height: 104.8px;" src="../assets/logo.png"/></div>
           </div>

          <!-- <button @click="toggleSidebar">&times;</button> -->
        </div>
        <ul class="sidebar-menu">
          <li><router-link to="/campusOpinion">首页</router-link></li>
          <li><router-link to="/mappingKnowledge">知识图谱</router-link></li>
          <li><router-link to="/schoolOpinion">校园舆情信息</router-link></li>
          <li><router-link to="/opinionInformation">舆情信息列表</router-link></li>
          <li><router-link to="/riskPerson">人物精准画像</router-link></li>
          <li>
            <router-link to="/riskTask">复杂网络分析</router-link>
          </li>
        </ul>
      </aside>

      <!-- 主内容区域 -->
      <main class="main-content">
        <!-- <button @click="toggleSidebar" class="sidebar-toggle">
          &#9776;
        </button> -->
        <div class="content">
          <router-view></router-view>
        </div>
      </main>
    </div>
  </template>

<script>

export default {
  name: 'indexVue',
  data () {
    return {
      isSidebarOpen: true

    }
  },
  methods: {
    toggleSidebar () {
      this.isSidebarOpen = !this.isSidebarOpen
    }
  }
}
</script>

<style lang="less" scoped>
.wrapper {
  display: flex;
}

.sidebar {
  width: 250px;
  height: 100vh;
  position: fixed;
  left: -250px;
  transition: left 0.3s ease-in-out;
  background-color: #103a66;
  color: #fff;
  overflow-y: auto;
}

.sidebar.active {
  left: 0;
}

.sidebar-header {

  background-color: #ececec;
  height: 100px;
}

.sidebar-header h3 {
  margin: 0 auto;
}

.sidebar-menu {
  list-style: none;
  padding: 0;

}

.sidebar-menu li a {
  display: block;
  text-align: left;

  padding: 10px 50px;
  color: #fff;
  text-decoration: none;
  line-height: 60px;
}
.sidebar-menu li a.router-link-active{
      color:orange
    }
.sidebar-menu li a:hover {
  background-color: #555;
}

.main-content {
  margin-left: 250px;
  padding: 20px;
  transition: margin-left 0.3s ease-in-out;
}

.sidebar-toggle {
  position: fixed;
  top: 10px;
  left: 10px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    left: -100%;
  }

  .sidebar.active {
    left: 0;
  }

  .main-content {
    margin-left: 0;
  }
}
</style>

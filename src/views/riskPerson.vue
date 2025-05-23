<template>
  <div class="box">
    <div class="box-head">
      <el-upload
        class="upload-demo"
        action="http://localhost:5000/get_label"
        :show-file-list="false"
        :http-request="uploadFile"
        :limit="3"
        accept=".xlsx">
          <el-link icon="el-icon-edit">上传用于动态计算人物心理健康等级</el-link>
      </el-upload>
    </div>
    <div class="box-foot">
        <div class="foot-mapping">
          <el-table
      :data="tableData"
      style="width: 100%"
      @row-click="handleRowClick">
      <el-table-column
        prop="id"
        label="ID"
       >
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
       >
      </el-table-column>
      <el-table-column
        prop="major"
        label="专业"
        >
      </el-table-column>
      <el-table-column
        prop="grade"
        label="年级"
        >
      </el-table-column>

    </el-table>
    <div class="block" style="text-align: center;">
             <el-pagination
               @size-change="handleSizeChange"
               @current-change="handleCurrentChange"
               :current-page="currentPage"
               :page-sizes="[10, 15, 20]"
               :page-size="10"
               layout="total, prev, pager, next"
               :total="total">
            </el-pagination>
        </div>
        </div>
        <div class="portrait" v-if="male || female">
          <img v-if="male" style="width: 80px; height: 80px;" src="../assets/male.png"/>
          <img v-if="female" style="width: 80px; height: 80px;" src="../assets/female.png"/>
          <p v-if="name.length == 3" style="margin: 0px 0px 0px 16px;">{{ name }}</p>
          <p v-if="name.length == 2" style="margin: 0px 0px 0px 22px;">{{ name }}</p>
        </div>
        <div class="img" v-if="male || female">
          <el-tag v-if="dataStatus.预测标签 == 0" type="success" effect="plain" >活力四射</el-tag>
          <el-tag v-else-if="dataStatus.预测标签 == 1" type="warning">情绪波动</el-tag>
          <el-tag v-else-if="dataStatus.预测标签 == 2" type="danger" effect="dark">心事重重</el-tag>
        </div>
        <div id="chart" class="foot-table">
          <!-- <e-charts class="chart" :option="option"/> -->
        </div>
    </div>
    <div>
      <el-dialog
          title="提示"
          :visible.sync="dialogVisible"
          width="90%"
          :before-close="handleClose"
          >
          <div style="display: flex;">
            <div class="foot-mapping1">
            <el-table
                :data="tableData"
                style="width: 500px"
                @row-click="handleRowClick1">
                <el-table-column
                  label="ID"
                  :render-header="renderHeader">
                  <template slot-scope="scope">
                    {{ scope.$index + 1 }}  <!-- 自定义 ID 从 1 开始 -->
                  </template>
                </el-table-column>
                <el-table-column
                prop="name"
                label="姓名"
              >
            </el-table-column>
            <el-table-column
              prop="major"
              label="专业"
              >
            </el-table-column>
            <el-table-column
              prop="grade"
              label="年级"
              >
            </el-table-column>

            </el-table>
          </div>
          <div class="portrait1" v-if="male || female">
          <img v-if="male" style="width: 80px; height: 80px;" src="../assets/male.png"/>
          <img v-if="female" style="width: 80px; height: 80px;" src="../assets/female.png"/>
          <p v-if="name.length == 3" style="margin: 0px 0px 0px 16px;">{{ name }}</p>
          <p v-if="name.length == 2" style="margin: 0px 0px 0px 22px;">{{ name }}</p>
          </div>
          <div class="img1" v-if="male || female">
          <el-tag v-if="dataStatus1.预测标签 == 0" type="success" effect="plain" >活力四射</el-tag>
          <el-tag v-else-if="dataStatus1.预测标签 == 1" type="warning">情绪波动</el-tag>
          <el-tag v-else-if="dataStatus1.预测标签 == 2" type="danger" effect="dark">心事重重</el-tag>
          </div>
          <div id="chart1" class="foot-table1">
          <!-- <e-charts class="chart" :option="option"/> -->
          </div>
          </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { postStudentOpinion } from '@/api/studentMessage'
import axios from 'axios'
export default {

  data () {
    return {
      dialogVisible: false,
      dataStatus: {
        学习程度: -0.1,
        考试压力: -0.1,
        情绪波动: -0.1,
        帮助支持: -0.1,
        心理帮助: -0.1,
        日常困难: -0.1,
        预测标签: 4
      }, // 用于存储后端传来的数据
      dataStatus1: {
        学习程度: -0.1,
        考试压力: -0.1,
        情绪波动: -0.1,
        帮助支持: -0.1,
        心理帮助: -0.1,
        日常困难: -0.1,
        预测标签: 4
      }, // 用于存储后端传来的数据
      legendData: [], // 用于存储图例数据
      tableData: [{
      }],
      currentPage: 1,
      total: 10,
      pageSize: 9,
      sign: 0,
      male: false,
      female: false,
      name: ''
    }
  },
  mounted () {
    this.pageQuery()
  },
  methods: {
    handleClose () {
      location.reload()
    },
    renderHeader (h) {
      return h('span', 'ID') // 定义列头
    },
    uploadFile (param) {
      // 手动上传文件
      const formData = new FormData()
      formData.append('file', param.file)
      axios.post('http://localhost:5000/get_label', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        // this.anticipatedData = response.data
        console.log('后端返回的数据：', response.data)
        this.dialogVisible = true
        this.male = false
        this.female = false
        this.name = ''
        this.currentPage = Math.ceil(Math.random() * 5 + 3)
        this.pageSize = response.data.result
        this.pageQuery1()
      }).catch((err) => {
        console.log('上传过程中发生错误：', err)
      })
    },
    pageQuery1 () {
      const paramsObj = {
        page: this.currentPage,
        pageSize: this.pageSize
      }
      console.log(paramsObj)
      postStudentOpinion(paramsObj).then(res => {
        if (res.data.code === 1) {
          this.total = res.data.data.total
          this.tableData = res.data.data.records
          console.log(this.tableData)
          this.initChart1()
        }
      }).catch(err => {
        this.$message.error('请求出错了：' + err.message)
        console.log(err.message)
      })
    },
    pageQuery () {
      const paramsObj = {
        page: this.currentPage,
        pageSize: this.pageSize
      }
      console.log(paramsObj)
      postStudentOpinion(paramsObj).then(res => {
        if (res.data.code === 1) {
          this.total = res.data.data.total
          this.tableData = res.data.data.records
          console.log(this.tableData)
          this.initChart()
        }
      }).catch(err => {
        this.$message.error('请求出错了：' + err.message)
        console.log(err.message)
      })
    },
    handleSizeChange (val) {
      this.pageSize = val
      this.pageQuery()
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.pageQuery()
      console.log(`当前页: ${val}`)
    },
    async handleRowClick (row) {
      this.male = false
      this.female = false
      // console.log('你点击了行数据：', row.id)
      // const response = await axios({
      //   method: 'post',
      //   url: 'https://localhost:5000/get_label', // 后端 API 地址
      //   data: { number: row.id }, // 请求体数据，可以是任何你需要的参数
      //   headers: {
      //     'Content-Type': 'application/json'
      //   }
      // })

      // // 打印返回的结果
      // console.log('Response:', response.data)

      // // 将返回的数据存储到 data 中
      // this.responseData = response.data
      this.name = row.name
      try {
        // 发送 POST 请求到后端 /get_label 接口
        const response = await axios.post('http://localhost:5000/get_label', {
          number: row.id
        })

        // 打印后端响应并存储
        console.log('后端响应:', response.data)
        this.dataStatus = response.data
        if (row.sex === '男') {
          this.male = true
        }
        if (row.sex === '女') {
          this.female = true
        }
      } catch (error) {
        // 捕获错误并输出
        console.error('请求失败:', error)
        this.response = '请求失败，请检查控制台错误'
      }

      if (row.id <= 9) {
        this.sign = row.id - 1
        this.initChart()
      } else {
        this.sign = (row.id - 1) % 9
        this.initChart()
      }
    },
    async handleRowClick1 (row) {
      this.male = false
      this.female = false
      // console.log('你点击了行数据：', row.id)
      // const response = await axios({
      //   method: 'post',
      //   url: 'https://localhost:5000/get_label', // 后端 API 地址
      //   data: { number: row.id }, // 请求体数据，可以是任何你需要的参数
      //   headers: {
      //     'Content-Type': 'application/json'
      //   }
      // })

      // // 打印返回的结果
      // console.log('Response:', response.data)

      // // 将返回的数据存储到 data 中
      // this.responseData = response.data
      this.name = row.name
      try {
        // 发送 POST 请求到后端 /get_label 接口
        const response = await axios.post('http://localhost:5000/get_label', {
          number: row.id - 1
        })

        // 打印后端响应并存储
        console.log('后端响应:', response.data)
        this.dataStatus1 = response.data
        if (row.sex === '男') {
          this.male = true
        }
        if (row.sex === '女') {
          this.female = true
        }
      } catch (error) {
        // 捕获错误并输出
        console.error('请求失败:', error)
        this.response = '请求失败，请检查控制台错误'
      }

      if (row.id <= 9) {
        this.sign = row.id - 1
        this.initChart1()
      } else {
        this.sign = (row.id - 1) % 9
        this.initChart1()
      }
    },
    initChart () {
      const myChart = echarts.init(document.getElementById('chart'))
      const option = {
        title: {
          text: '人物分析雷达图'
        },
        radar: {
          // shape: 'circle',
          indicator: [
            { name: '学习程度', max: 1.1 },
            { name: '就业，升学压力', max: 1.1 },
            { name: '情绪波动', max: 1.1 },
            { name: '帮助支持', max: 1.1 },
            { name: '心理帮助', max: 1.1 },
            { name: '生活，人际困难', max: 1.1 }
          ]
        },
        series: [
          {
            type: 'radar',
            data: [
              {
                value: [this.dataStatus.学习程度 + 0.1, this.dataStatus.考试压力 + 0.1, this.dataStatus.情绪波动 + 0.1, this.dataStatus.帮助支持 + 0.1, this.dataStatus.心理帮助 + 0.1, this.dataStatus.日常困难 + 0.1]

              }

            ]
          }
        ]
      }
      myChart.setOption(option)
    },
    initChart1 () {
      const myChart1 = echarts.init(document.getElementById('chart1'))
      const option1 = {
        title: {
          text: '人物分析雷达图'
        },
        radar: {
          // shape: 'circle',
          indicator: [
            { name: '学习程度', max: 1.1 },
            { name: '就业，升学压力', max: 1.1 },
            { name: '情绪波动', max: 1.1 },
            { name: '帮助支持', max: 1.1 },
            { name: '心理帮助', max: 1.1 },
            { name: '生活，人际困难', max: 1.1 }
          ]
        },
        series: [
          {
            type: 'radar',
            data: [
              {
                value: [this.dataStatus1.学习程度 + 0.1, this.dataStatus1.考试压力 + 0.1, this.dataStatus1.情绪波动 + 0.1, this.dataStatus1.帮助支持 + 0.1, this.dataStatus1.心理帮助 + 0.1, this.dataStatus1.日常困难 + 0.1]

              }

            ]
          }
        ]
      }
      myChart1.setOption(option1)
    }
  }
}
</script>
<style lang="less" scoped>
.el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
.box-head{
    display: flex;
    width: 1200px;
    height: 50px;
    margin: 0 0 0 60px;
}
.box-foot{
    display: flex;
    widows: 1200px;
    .foot-mapping{
        width: 500px;
        height: 600px;
        border: 1px solid #000;
        margin: 0 70px 0 60px ;
    }
    .foot-table{
        width: 600px;
        height: 600px;
        border: 1px solid #000;
        .el-pagination{
            text-align: center;
        }
    }
}
.foot-mapping1{
  width: 500px;
        height: 600px;
        border: 1px solid #000;
        margin: 0 70px 0 60px ;
}
.foot-table1{
  width: 600px;
        height: 600px;
        border: 1px solid #000;
        .el-pagination{
            text-align: center;
        }
}
.portrait{
  position: absolute;
  top: 120px;
  right: 500px;

}
.portrait1{
  position: absolute;
  top: 120px;
  right: 600px;

}
.img{
  position: absolute;
  top:150px;
  right: 50px;
}
.img1{
  position: absolute;
  top:150px;
  right: 150px;
}
</style>

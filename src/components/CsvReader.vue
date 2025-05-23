<template>
  <div>
    <div style="display: flex; justify-content: space-between;">
      <div><el-button  icon="el-icon-refresh-left" @click="refreshData">刷新</el-button></div>
      <div><el-button type="success"  @click="dialogFormVisible = true" >上传单条文本</el-button></div>
      <el-upload

        class="upload-demo"
        action="http://localhost:5000/predict"
        :http-request="addFile"
        :limit="3"

        >
        <el-button icon="el-icon-upload2"  type="primary" style="margin-right: 20px;">上传文本文件</el-button>
      </el-upload>
      <div style="display: flex;">
        <div>
          <el-form >
              <el-form-item>
                    <el-select v-model="classification" placeholder="舆情分类" >
                      <el-option label="交通事故" value="交通事故"></el-option>
                      <el-option label="校管事件" value="校管事件"></el-option>
                      <el-option label="教学管理" value="教学管理"></el-option>
                      <el-option label="人身安全" value="人身安全"></el-option>
                    </el-select>
               </el-form-item>
            </el-form>
        </div>
            <el-button icon="el-icon-search" circle @click="submit" style="margin: 0 10px; height:40px ;">
            </el-button>
      </div>

    </div>
    <el-table :data="randomData" style="width: 100%">
      <el-table-column width="100px" prop="label" label="情感">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.label == 1">正面</el-tag>
          <el-tag v-else-if="scope.row.label == 0" type="danger">负面</el-tag>
          <el-tag v-else type="warning">未知</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="review" label="文本">
      </el-table-column>
    </el-table>
    <el-dialog :title="gridData.eventType" :visible.sync="dialogTableVisible">
                    <el-table
                         :data="gridData"
                         style="width: 100%"
                         >
                         <el-table-column
                             prop="time"
                             label="时间"
                             width="200">
                         </el-table-column>
                         <el-table-column
                             prop="place"
                             label="地点"
                             width="200">
                         </el-table-column>
                         <el-table-column
                              prop="courseEvent"
                              label="事件经过"
                              width="200">
                         </el-table-column>
                         <el-table-column
                             prop="handleSchool"
                             label="校方处理"
                             width="200">
                         </el-table-column>
                         <el-table-column
                             prop="socialImpact"
                             label="社会影响"
                             width="200">
                         </el-table-column>
                    </el-table>
                    <div class="block">
                      <el-pagination
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page="currentPage"
                        :page-sizes="[5, 10, 15, 20]"
                        :page-size="pageSize"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="total">
                      </el-pagination>
                    </div>
    </el-dialog>
    <el-dialog title="输入舆情信息用于判定属性" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="舆情文本" :label-width="formLabelWidth">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入舆情文本信息"
              v-model="form.text">
            </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="UnSentimentInformation">取 消</el-button>
          <el-button type="primary" @click="SentimentInformation">确 定</el-button>
        </div>
  </el-dialog>
  <el-dialog title="舆情展示" :visible.sync="dialogInformationVisible">
          <el-tag v-if="isInformation == 1">正面</el-tag>
          <el-tag v-else-if="isInformation == 0" type="danger">负面</el-tag>
          <el-tag v-else type="warning">未知</el-tag>
          {{ form.text }}
          <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="secede">确 定</el-button>
        </div>
  </el-dialog>
  <el-dialog title="舆情展示" :visible.sync="dialogsInformationVisible" width="600px">
    <AnticipatedDisplay :parent-message="anticipatedData"></AnticipatedDisplay>
  </el-dialog>
  </div>
</template>

<script>
import { getOpinionInformation } from '@/api/opinionInformation'
import { postSchoolOpinion } from '@/api/schoolOpinion'
import AnticipatedDisplay from '@/components/AnticipatedDisplay.vue'
import axios from 'axios'
export default {
  components: {
    AnticipatedDisplay
  },
  data () {
    return {
      randomData: [],
      classification: '',
      dialogInformationVisible: false,
      dialogTableVisible: false,
      dialogFormVisible: false,
      dialogsInformationVisible: false,
      currentPage: 1,
      pageSize: 5,
      total: 5,
      anticipatedData: [
        {
          text: 'ss',
          sentiment_code: 0
        },
        {
          text: 'ss',
          sentiment_code: 1
        }
      ],
      gridData: [],
      formLabelWidth: '120px',
      form: {
        text: ''
      },
      isInformation: ''
    }
  },
  methods: {
    addFile (param) {
      // 手动上传文件
      const formData = new FormData()
      formData.append('file', param.file)
      axios.post('http://localhost:5000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        // this.anticipatedData = response.data
        console.log('后端返回的数据：', response.data)
        this.dialogsInformationVisible = true
        const convertedData = Object.keys(response.data).map(key => {
          const parts = key.split(':')
          const text = parts[1]
          const sentiment = response.data[key].split(':')[1]
          return {
            text: text,
            sentiment_code: sentiment
          }
        })
        this.anticipatedData = convertedData
        console.log(this.anticipatedData)
      }).catch((err) => {
        console.log('上传过程中发生错误：', err)
      })
    },
    secede () {
      this.dialogInformationVisible = false
      this.form = {
        text: ''
      }
    },
    handleSuccess (response, file, fileList) {
      this.dialogsInformationVisible = true
      this.anticipatedData = response.data
      console.log(response.data)
    },
    SentimentInformation () {
      const paramsObj = { text: this.form.text }

      postSchoolOpinion(paramsObj).then(res => {
        console.log(res.data)
        const parts = res.data.sentiment_code.split('(')[1].split(')')[0]
        this.isInformation = parseInt(parts)
        // this.isInformation = res.data

        this.dialogFormVisible = false
        this.dialogInformationVisible = true
      }).catch(error => {
        this.dialogFormVisible = false
        console.error(error)
      })
    },
    UnSentimentInformation () {
      this.dialogFormVisible = false
      this.form = {
        text: ''
      }
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    submit () {
      this.gridData.eventType = this.classification
      this.dialogTableVisible = true
      this.opinionInformationPageQuery()
    },
    opinionInformationPageQuery () {
      const paramsObj = { page: this.currentPage, pageSize: this.pageSize, classification: this.classification }
      getOpinionInformation(paramsObj).then(res => {
        if (res.data.code === 1) {
          this.total = res.data.data.total
          this.gridData = res.data.data.records
        }
      }).catch(err => {
        this.$message.error('请求出错了：' + err.message)
        console.log(err.message)
      })
    },
    async fetchData () {
      try {
        const response = await this.$http.get('/Campus_public_opinion_text_corpus.csv')

        const rows = response.data.split('\n')

        const header = rows[0].split(',')

        const data = rows.slice(1).map(row => {
          const values = row.split(',')
          return header.reduce((obj, key, index) => {
            obj[key] = values[index]
            return obj
          }, {})
        })
        this.randomData = this.getRandomSubarray(data, 20)
        console.log(this.randomData)
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    },
    getRandomSubarray (arr, size) {
      const shuffled = arr.slice(0); let i = arr.length; let temp; let index
      while (i--) {
        index = Math.floor((i + 1) * Math.random())
        temp = shuffled[index]
        shuffled[index] = shuffled[i]
        shuffled[i] = temp
      }
      return shuffled.slice(0, size)
    },
    refreshData () {
      this.fetchData()
    },
    handleSizeChange (val) {
      this.pageSize = val
      this.opinionInformationPageQuery()
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.opinionInformationPageQuery()
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>

<style scoped>
.label1{
  width: 100px;
}
</style>

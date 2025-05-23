<template>
  <div class="box">

    <div class="box-head">
        <h2>各高校舆情信息列表</h2>
      <div style="display:flex;">
        <p style="margin: 23px 0 0 40px;">时间范围：</p>
        <div style="margin: 20px 5px">
          <el-radio-group v-model="timeHorizon" size="medium">
          <!-- <el-radio-button label="24小时" ></el-radio-button> -->
          <el-radio-button label="今天"></el-radio-button>
          <el-radio-button label="昨天"></el-radio-button>
          <el-radio-button label="前三天"></el-radio-button>
          <el-radio-button label="近七天"></el-radio-button>
          <el-radio-button label="近30天"></el-radio-button>
        </el-radio-group>
        <el-button style="width: 83px; height: 35.6px; " @click="dialogVisible = true">自定义</el-button>
      </div>
      </div>
      <el-dialog :visible.sync="dialogVisible" title="自定义日期" width="30%">
      <el-date-picker
        v-model="date"
        type="date"
        placeholder="选择日期">
      </el-date-picker>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button @click="handleConfirm">确定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="添加舆情信息" :visible.sync="dialogTableVisible">
      <el-form ref="form" :model="form" label-width="80px">
  <el-form-item label="发生地点">
    <el-input v-model="form.place" placeholder="请输入发生地点"></el-input>
  </el-form-item>
  <el-form-item label="事件类型">
    <el-select v-model="form.classification" placeholder="请选择事件类型">
      <el-option label="交通事故" value="交通事故"></el-option>
      <el-option label="校管事件" value="校管事件"></el-option>
      <el-option label="教学管理" value="教学管理"></el-option>
      <el-option label="人身安全" value="人身安全"></el-option>
    </el-select>
  </el-form-item>
  <el-form-item label="发生时间">
    <el-col :span="11">
      <el-date-picker type="date" placeholder="选择日期" v-model="form.timeHorizon" style="width: 100%;"></el-date-picker>
    </el-col>

  </el-form-item>
  <el-form-item label="事件经过" >
    <el-input type="textarea" v-model="form.courseEvent" placeholder="请输入事件经过"></el-input>
  </el-form-item>
  <el-form-item label="校方处理" >
    <el-input type="textarea" v-model="form.handleSchool" placeholder="请输入校方处理"></el-input>
  </el-form-item>
  <el-form-item label="社会影响" >
    <el-input type="textarea" v-model="form.socialImpact" placeholder="请输入社会影响"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="addSubmit">添加</el-button>
    <el-button @click="unAddSubmit">取消</el-button>
  </el-form-item>
</el-form>
    </el-dialog>
    <el-dialog
  title="确认删除"
  :visible.sync="deleteDialogVisible"
  width="300px"
>
  <span>是否确认删除选中行？</span>
  <span slot="footer">
    <el-button @click="batchDelete">确认</el-button>
    <el-button @click="deleteDialogVisible = false">取消</el-button>
  </span>
</el-dialog>
      <div class="headButton">
        <div class="headButton1">
          <el-input class="input1" v-model="place"  placeholder="发生地点"></el-input>
          <el-input class="input2" v-model="context"  placeholder="事件经过"></el-input>
              <el-form >
                <el-form-item>
                      <el-select v-model="classification" placeholder="事件类型">
                        <el-option label="交通事故" value="交通"></el-option>
                        <el-option label="校管事件" value="校管"></el-option>
                        <el-option label="教学管理" value="教学"></el-option>
                        <el-option label="人身安全" value="人身"></el-option>

                      </el-select>
                 </el-form-item>
            </el-form>
          </div>
        <div class="headButton2"><el-button @click="reset">重置</el-button>
          <el-button type="primary" @click="submit">提交</el-button></div>
      </div>
      <div class="footButton">
        <el-button class="footButton1" type="primary" icon="el-icon-edit" @click="dialogTableVisible = true">添加</el-button>
        <el-button class="footButton2" type="danger" icon="el-icon-delete" @click="deleteDialogVisible = true">批量删除</el-button>
      </div>
    </div>
    <div class="box-foot">
      <el-table
                         :data="gridData"
                         style="width: 100%"
                         :row-key="row => row.id"
                         @selection-change="handleSelectionChange"
                         >
                         <el-table-column
                             type="selection"
                             width="55"
                             >
                          </el-table-column>
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
                              prop="eventType"
                              label="事件类型"
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
               :page-size="5"
               layout="total, sizes, prev, pager, next, jumper"
               :total="total">
            </el-pagination>
        </div>
    </div>
  </div>
</template>

<script>
import { getOpinionInformation, addOpinionInformation, deleteOpinionInformation } from '@/api/opinionInformation'
const cityOptions = ['正面', '负面', '中性']
export default {
  data () {
    return {
      selectedRows: [], // 存储选中行数据
      form: [{
        place: '', // 地点
        classification: '', // 事件类型
        timeHorizon: '', // 发生时间
        courseEvent: '', // 事件经过
        handleSchool: '', // 校方处理
        socialImpact: '' // 社会处理
      }],
      deleteDialogVisible: false, // 删除确认对话框
      dialogTableVisible: false, // 添加的对话框
      dialogVisible: false, // 自定义时间的对话框
      date: new Date(), // 设置默认日期为当前日期
      timeHorizon: '',
      checkAll: false,
      checkedCities: ['正面'],
      cities: cityOptions,
      isIndeterminate: true,
      checkList: [],
      place: '',
      context: '',
      classification: '',
      gridData: [{
      }],
      currentPage: 1,
      total: 5,
      pageSize: 5
    }
  },
  created () {
    this.pageQuery()
  },
  methods: {
    batchDelete () {
      if (this.selectedRows.length === 0) {
        this.$message.warning('请先选择要删除的行！')
        this.deleteDialogVisible = false
        return
      }
      // 假设后端有批量删除接口，如 /api/batchDelete，需根据实际修改
      const ids = this.selectedRows.map(row => row.id)
      console.log(ids.join(','))
      deleteOpinionInformation(ids)
        .then(res => {
          if (res.data.code === 1) {
            this.$message.success('批量删除成功')
            this.selectedRows = [] // 清空选中行
            this.pageQuery() // 刷新表格数据
            this.deleteDialogVisible = false
          } else {
            this.$message.error('批量删除失败：' + res.data.message)
          }
        })
        .catch(err => {
          this.$message.error('请求出错：' + err.message)
        })
    },
    unAddSubmit () {
      this.dialogTableVisible = false
      this.form = [{
        place: '',
        eventType: '',
        time: '',
        courseEvent: '',
        handleSchool: '',
        socialImpact: ''
      }]
    },
    addSubmit () {
      addOpinionInformation(this.form).then(res => {
        if (res.data.code === 1) {
          this.$message.success('添加成功')
          this.dialogTableVisible = false
          this.form = []
          this.pageQuery()
        }
      }).catch(err => {
        this.$message.error('请求出错了：' + err.message)
        console.log(err.message)
      })
    },
    submit () {
      this.pageQuery()
    },
    pageQuery () {
      const paramsObj = {
        place: this.place,
        context: this.context,
        page: this.currentPage,
        pageSize: this.pageSize,
        classification: this.classification,
        timeHorizon: this.timeHorizon
      }
      console.log(paramsObj)
      getOpinionInformation(paramsObj).then(res => {
        if (res.data.code === 1) {
          this.total = res.data.data.total
          this.gridData = res.data.data.records
          console.log(this.gridData)
        }
      }).catch(err => {
        this.$message.error('请求出错了：' + err.message)
        console.log(err.message)
      })
    },

    reset () {
      // eslint-disable-next-line no-unused-expressions, no-sequences
      this.place = '',
      this.context = '',
      this.checkedCities = [],
      this.timeHorizon = '',
      this.classification = '',
      this.pageQuery()
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
    handleCheckAllChange (val) {
      this.checkedCities = val ? cityOptions : []
      this.isIndeterminate = false
    },
    handleConfirm () {
      this.timeHorizon = this.date
      console.log('您选择的日期是：', this.date)
      this.pageQuery()
      this.dialogVisible = false
    },
    handleSelectionChange (rows) {
      this.selectedRows = rows
      console.log(this.selectedRows)
    }
  }

}

</script>

<style lang="less" scoped>
.el-table {
    .warning-row {
    background: oldlace;
  }
}

  .el-table  {
    .success-row{
      background: #f0f9eb;
    }
  }
.box-head {
    width: 1200px;
    background-color: #ffffff;
    height: 300px;
    margin: 15px;
    border: 1px solid #f8f8f8;
    box-shadow: 0 0 100px 100px #f8f8f8;
}
.timeList {
  display: flex;
  list-style-type: none;
  gap: 10px;
  .li1{
    padding:5px 0 0 0
  }
}
.emoList{
    display: flex;
    .span1{
        margin: 0 15px 0 40px;
    }
}
.footButton{
  margin-left: 40px;
  .footButton1{
    margin-right: 20px;
  }
}
.headButton{
    display: flex;
    padding: 20px 0 0 0 ;
    .headButton2{
      width: 200px;
    }
    .headButton1{
      display: flex;
      .input1{
        width: 200px;
        margin: 0 20px 0 40px;
      }
      .input2{
        width: 200px;
        margin: 0 20px 0 0px;
      }
      .el-form{
        width: 200px;
        margin: 0 100px 0 0 ;
      }
    }
}
.box-foot{
    width: 1200px;
    margin: 15px;
}

</style>

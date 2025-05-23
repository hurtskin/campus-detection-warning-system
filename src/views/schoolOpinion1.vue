<template>
  <div class="class">
     <div class="box-campus">
         <div class="campusFirst">
             <h2>校园舆情信息</h2>
             <div><CsvReader></CsvReader></div>
         </div>
  </div>
  </div>
 </template>

<script>
import CsvReader from '@/components/CsvReader.vue'
export default {
  components: {
    CsvReader
  }
}
</script>

 <style lang="less" scoped>
 .block{
     text-align: center;
 }
 .box-campus{
     width: 1200px;
     background-color: #ffffff;
     border: 1px solid #f8f8f8;
     box-shadow: 0 0 100px 100px #f8f8f8;
     margin: 0 auto;
     .campusInput{
         display: flex;
         padding: 15px 0 0 0;
         .el-checkbox{
             width: 4000px;
             padding: 0 0 0 40px;
         }
     }
     .campusFoot{
         .campusInfo{
             .InfoCommit{
                 display: flex;
                 margin: 0;
                 .el-checkbox{
                 padding: 23px 10px 0 40px;
                 }
                 }
             }
             p{
                 padding: 0 0 0 65px ;
                 margin: 0;
                 color: #808080;
             }
             .detInfo{
                 display: flex;
                 span{
                     color: #808080;
                     margin: 10px 25px;
                 }
                 .el-tag{
                     margin: 8px 25px 0 60px;
                 }

             }
         }
     }

 </style>

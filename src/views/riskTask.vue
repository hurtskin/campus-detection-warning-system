<template>
  <div>
      <div style="display: flex; width: 1200px;" v-if="nameNumber != 5">
        <!-- <div style="width: 300px;"><el-button>默认按钮</el-button></div> -->
        <div style="height: 300px; width: 350px">
          <el-card  class="page-navigation">
            <div @click="skip_one" class="active">
              <span>①</span><span>热血高校人物关系图谱</span>
              <div style="display: block; margin-left: 7px"><p style="margin: 0px; padding: 0px;" >|</p><p style="margin: 0px; padding: 0px;">|</p></div>
            </div>
            <div @click="skip_two" :class="nameNumber != 1 ? 'active' : ''">
              <span>②</span><span>热血高校人物关系图谱挖掘出的风险社团</span>
              <div style="display: block; margin-left: 7px"><p style="margin: 0px">|</p><p style="margin: 0px">|</p></div>
            </div>
            <div @click="skip_three" :class="nameNumber != 1 && nameNumber != 2 ? 'active' : ''">
              <span>③</span><span>挖出风险社团的过程</span>
              <div style="display: block; margin-left: 7px"><p style="margin: 0px">|</p><p style="margin: 0px">|</p></div>
            </div>
            <div @click="skip_four" :class="nameNumber == 4 ? 'active' : ''">
              <span>④</span><span>热血高校人物关系图谱挖掘出的风险社团详细版</span>
              <div style="display: block; margin-left: 7px"><p style="margin: 0px">|</p><p style="margin: 0px">|</p></div>
            </div>
            <div @click="skip_five"><span>⑤</span><span>挖掘的真实风险社团图谱，接近中心性关系图谱，介数中心性关系图谱</span></div>
          </el-card>
          <div style="margin-top: 50px">
            <el-card class="page-container">
              <p style="font-size: 10px">上传文件处可进行图标的修改,需要两个txt文件一个用于属性，另一个用于列表</p>
              <div style="margin: 20px 0px 0px 110px;"><el-button type="primary" @click="drawer = true">上传<i class="el-icon-upload el-icon--right"></i></el-button></div>
            </el-card>
          </div>
          <el-drawer
              title="文件上传处"
              :visible.sync="drawer"
              direction="ltr"
              :before-close="handleClose">
              <el-upload
                class="upload-demo"
                drag
                action="http://localhost:5000/upAttributes"
                :limit="5"
                accept=".txt"
                :on-success="handleUploadAttributes"
                :file-list="upAttributesList">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将属性.txt文件拖到此处，或<em>点击上传</em></div>
              </el-upload>
              <el-upload
                class="upload-demo"
                drag
                action="http://localhost:5000/upEdgelist"
                :limit= "5"
                accept=".txt"
                :on-success="handleUploadEdgelist"
                :file-list="upEdgeList">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将列表.txt文件拖到此处，或<em>点击上传</em></div>
              </el-upload>

              <div style="margin: 30px 0 0 255px">
                <el-button @click="handleClose">取消</el-button>
                <el-button type="primary" @click="getUploadAction(nameNumber)">提交</el-button>
              </div>
          </el-drawer>

      </div>
        <div>
          <el-card class="page-container"  v-loading="loading" v-if="nameNumber != 5">
            <div v-if="nameNumber == 1 && globalGraphSeries.links && globalGraphSeries.nodes" class="node_embedding_charts" ><globalGraph :value="globalGraphSeries"></globalGraph></div>
            <div v-if="nameNumber == 2" class="sub_graph"><MinedCommunityGraph :value="minedCommunityGraphSeries"></MinedCommunityGraph></div>
            <div v-if="nameNumber == 3" class="global_graph" ><NodeEmbeddingCharts :value="nodeEmbeddingChartsSeries"></NodeEmbeddingCharts></div>
            <div v-if="nameNumber == 4" class="centrality_graphs"><SubGraph :value="subGraphSeries"></SubGraph></div>
          </el-card>
        </div>
      </div>
      <div v-if="nameNumber == 5" >
        <div style="width: 1200px;">
        <el-steps :active="nameNumber">
            <el-step  description="热血高校人物关系图谱"></el-step>
            <el-step  description="热血高校人物关系图谱挖掘出的风险社团"></el-step>
            <el-step  description="挖出风险社团的过程"></el-step>
            <el-step  description="热血高校人物关系图谱挖掘出的风险社团详细版"></el-step>
            <el-step  description="挖掘的真实风险社团图谱，接近中心性关系图谱，介数中心性关系图谱"></el-step>
        </el-steps>
      </div>
      <div v-if="nameNumber == 5" class="Mined_community_graph"><CentralityGraphs :value1="centralityGraphsSeries1"></CentralityGraphs></div>

      <div style="display: flex;">
        <div @click="skip_one"><i size="medium" class="el-icon-caret-left"></i>返回</div>
      <div style="margin-left: 820px; margin-top: 12px;">
        <el-upload
          class="upload-demo1"
          action="http://localhost:5000/upAttributes"
          :limit="3"
          :on-exceed="handleExceed"
          >
          <el-button size="small" type="primary">属性上传</el-button>
        </el-upload>
       </div>
       <div style="margin-left: 50px; margin-top: 12px;">
        <el-upload
          class="upload-demo1"
          action="http://localhost:5000/upEdgelist"
          :limit="3"
          :on-exceed="handleExceed"
          >
          <el-button size="small" type="primary">列表上传</el-button>
        </el-upload>
       </div>
       <div style="margin-left: 50px; margin-top: 8px;"><el-button @click="getUploadAction(nameNumber)" icon="el-icon-upload2" circle></el-button></div>
      </div>
      </div>

  </div>
</template>

<script>
import NodeEmbeddingCharts from '@/components/NodeEmbeddingCharts.vue'
import SubGraph from '@/components/SubGraph.vue'
import globalGraph from '@/components/GlobalGraph.vue'
import MinedCommunityGraph from '@/components/MinedCommunityGraph.vue'
import CentralityGraphs from '@/components/CentralityGraphs.vue'
import axios from 'axios'
export default {
  components: {
    NodeEmbeddingCharts,
    SubGraph,
    globalGraph,
    MinedCommunityGraph,
    CentralityGraphs
  },
  data () {
    return {
      upAttributesList: [],
      upEdgeList: [],
      uploadNumber: 0,
      drawer: false,
      loading: false,
      nameNumber: 1,
      actionPath: '',
      globalGraphSeries:
        {
          links: [
            {
              source: '1',
              target: '111',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '2',
              target: '4',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '2',
              target: '41',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '3',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '2',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '7',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '13',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '18',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '4',
              target: '21',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '6',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '6',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '2',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '4',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '13',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '18',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '7',
              target: '21',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '9',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '21',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '13',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '8',
              target: '22',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '9',
              target: '119',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '168',
              target: '122',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '118',
              target: '141',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '128',
              target: '145',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '138',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '118',
              target: '159',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '10',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '11',
              target: '122',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '11',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '12',
              target: '33',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '2',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '4',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '7',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '18',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '13',
              target: '21',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '21',
              target: '2',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '21',
              target: '4',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '21',
              target: '13',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '21',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '21',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '21',
              target: '18',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '14',
              target: '18',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '114',
              target: '131',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '14',
              target: '33',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '14',
              target: '51',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '114',
              target: '95',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '117',
              target: '98',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '119',
              target: '121',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '15',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '2',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '4',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '7',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '13',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '18',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '16',
              target: '21',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '19',
              target: '119',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '88',
              target: '115',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '24',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '29',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '36',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '40',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '42',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '122',
              target: '35',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '122',
              target: '38',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '122',
              target: '43',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '22',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '23',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '33',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '29',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '36',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '40',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '41',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '42',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '24',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '25',
              target: '125',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '125',
              target: '26',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '25',
              target: '26',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '26',
              target: '126',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '126',
              target: '30',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '26',
              target: '30',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '30',
              target: '130',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '30',
              target: '130',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '130',
              target: '32',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '32',
              target: '132',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '132',
              target: '130',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '34',
              target: '134',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '34',
              target: '35',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '135',
              target: '134',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '35',
              target: '135',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '35',
              target: '37',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '135',
              target: '137',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '137',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '38',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '137',
              target: '138',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '38',
              target: '138',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '38',
              target: '39',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '138',
              target: '139',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '39',
              target: '139',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '139',
              target: '43',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '139',
              target: '143',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '43',
              target: '143',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '43',
              target: '46',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '143',
              target: '146',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '46',
              target: '146',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '46',
              target: '47',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '146',
              target: '147',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '47',
              target: '147',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '150',
              target: '147',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '50',
              target: '47',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '50',
              target: '150',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '150',
              target: '151',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '50',
              target: '51',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '51',
              target: '151',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '151',
              target: '153',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '53',
              target: '51',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '53',
              target: '153',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '154',
              target: '153',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '53',
              target: '54',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '54',
              target: '154',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '154',
              target: '157',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '54',
              target: '57',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '57',
              target: '157',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '157',
              target: '160',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '57',
              target: '60',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '60',
              target: '160',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '160',
              target: '161',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '60',
              target: '61',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '61',
              target: '161',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '161',
              target: '162',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '61',
              target: '62',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '62',
              target: '162',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '162',
              target: '163',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '62',
              target: '63',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '63',
              target: '163',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '163',
              target: '164',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '63',
              target: '64',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '64',
              target: '164',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '164',
              target: '165',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '64',
              target: '65',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '65',
              target: '165',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '66',
              target: '65',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '66',
              target: '166',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '166',
              target: '167',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '67',
              target: '167',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '67',
              target: '68',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '167',
              target: '168',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '68',
              target: '168',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '69',
              target: '70',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '169',
              target: '170',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '69',
              target: '169',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '70',
              target: '170',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '70',
              target: '171',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '170',
              target: '171',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '71',
              target: '171',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '72',
              target: '73',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '172',
              target: '173',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '72',
              target: '172',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '73',
              target: '173',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '76',
              target: '176',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '76',
              target: '77',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '176',
              target: '177',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '177',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '78',
              target: '178',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '80',
              target: '180',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '81',
              target: '181',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '81',
              target: '77',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '181',
              target: '177',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '85',
              target: '185',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '86',
              target: '186',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '88',
              target: '188',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '88',
              target: '86',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '188',
              target: '186',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '89',
              target: '189',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '90',
              target: '190',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '91',
              target: '191',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '90',
              target: '89',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '190',
              target: '188',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '94',
              target: '194',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '95',
              target: '195',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '195',
              target: '196',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '94',
              target: '95',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '96',
              target: '196',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '196',
              target: '197',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '96',
              target: '97',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '97',
              target: '197',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '98',
              target: '198',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '199',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '97',
              target: '99',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '199',
              target: '197',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '102',
              target: '202',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '103',
              target: '203',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '104',
              target: '204',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '105',
              target: '210',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '105',
              target: '102',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '210',
              target: '103',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '106',
              target: '209',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '107',
              target: '106',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '107',
              target: '208',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '208',
              target: '206',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '108',
              target: '209',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '109',
              target: '206',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '109',
              target: '209',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '110',
              target: '205',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '111',
              target: '211',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '112',
              target: '217',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '110',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '111',
              target: '217',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '216',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '114',
              target: '215',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '115',
              target: '114',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '218',
              target: '113',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '115',
              target: '218',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '116',
              target: '219',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '116',
              target: '218',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '115',
              target: '219',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '117',
              target: '220',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '220',
              target: '221',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '117',
              target: '118',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '118',
              target: '221',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '119',
              target: '223',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '121',
              target: '223',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '122',
              target: '224',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '123',
              target: '225',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '125',
              target: '227',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '126',
              target: '228',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '128',
              target: '230',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '129',
              target: '231',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '80',
              target: '117',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '27',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '28',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '30',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '32',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '31',
              target: '33',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '39',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '141',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '31',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '57',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '88',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '102',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '105',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '110',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '121',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '158',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '131',
              target: '164',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '95',
              target: '178',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '95',
              target: '195',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '95',
              target: '197',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '97',
              target: '227',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '37',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '39',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '41',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '204',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '146',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '147',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '153',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '158',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '159',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '173',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '178',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '185',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '196',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '107',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '112',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '77',
              target: '121',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '88',
              target: '123',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '90',
              target: '138',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '91',
              target: '157',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '34',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '35',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '35',
              target: '59',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '38',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '141',
              target: '145',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '141',
              target: '148',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '58',
              target: '55',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '22',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '24',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '29',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '36',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '40',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '41',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '42',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '43',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '37',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '33',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '59',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '22',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '24',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '29',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '36',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '40',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '41',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '42',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '45',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '122',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '24',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '29',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '31',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '36',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '40',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '41',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '42',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '45',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '48',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '22',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '231',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '152',
              target: '158',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '33',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '37',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '52',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '89',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '99',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '145',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '152',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '186',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '207',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '113',
              target: '231',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '65',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '89',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '97',
              target: '99',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '145',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '152',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '186',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '207',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '99',
              target: '231',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '54',
              target: '155',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '55',
              target: '56',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '55',
              target: '49',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '55',
              target: '232',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '55',
              target: '233',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '55',
              target: '234',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '55',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '145',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '148',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '149',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '164',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '171',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '195',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '155',
              target: '197',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '1',
              target: '118',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '1',
              target: '133',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '37',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '44',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '59',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '234',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '233',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '33',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '37',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '52',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '44',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '232',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '232',
              target: '55',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '232',
              target: '56',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '232',
              target: '49',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '232',
              target: '233',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '232',
              target: '234',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '233',
              target: '234',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '233',
              target: '49',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '233',
              target: '55',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '233',
              target: '56',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '234',
              target: '56',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '234',
              target: '49',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '234',
              target: '232',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '234',
              target: '233',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '234',
              target: '58',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '234',
              target: '59',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '2',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '4',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '8',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '7',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '13',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '14',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '18',
              target: '21',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '58',
              target: '59',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '58',
              target: '37',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '58',
              target: '49',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '58',
              target: '234',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            },
            {
              source: '58',
              target: '16',
              emphasis: {},
              blur: {},
              select: {},
              ignoreForceLayout: false
            }
          ],
          nodes: [
            {
              name: '1',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '2',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u94dc\u5c9b\u5e7f\u6d77<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '3',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f\u7684\u6069\u4eba<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '4',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u4e09\u4e0a\u8c6a<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '6',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '7',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u725b\u5c71<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '8',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f<br/>label: 1<br/>Hierarchy: 2',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '9',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '10',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa\u7684\u540c\u5b66<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '11',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '12',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u82b9\u6cfd\u521d\u604b<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '13',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '14',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u8fde\u6cfd\u7460\u52a0<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '15',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa\u7684\u5f1f\u5f1f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '16',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u4e09\u4e0a\u5b66<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '18',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u7530\u6751\u5fe0\u592a<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '19',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '21',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '22',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u6797\u7530\u60e0<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '23',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1\u7684\u5973\u53cb<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '24',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '25',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '26',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '27',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5f3a\u7f57\u5f7b\u7684\u5802\u5144<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '28',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5f3a\u7f57\u5f7b\u7684\u53d1\u5c0f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '29',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u83c5\u7530\u548c\u5fd7<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '30',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '31',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '32',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '33',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u82b9\u6cfd\u591a\u6469\u96c4<br/>label: 1<br/>Hierarchy: 1',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '34',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '35',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '36',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '37',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u6cf7\u8c37\u6e90\u6cbb<br/>label: 1<br/>Hierarchy: 1',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '38',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '39',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '40',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u4e9a\u4e45\u6d25\u592a<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '41',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u9e6b\u5c3e\u4e61\u592a<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '42',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u955d\u6728\u65cb\u98ce\u96c4<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '43',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '44',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5742\u4e1c\u79c0\u4eba<br/>label: 1<br/>Hierarchy: 1',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '45',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5f3a\u7f57\u5f7b<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '46',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '47',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '48',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u8f6e\u5c9b\u77e2\u5c9b<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '49',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u7b52\u672c\u5c06\u6cbb<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '50',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '51',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '52',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u5c71\u5d0e\u8fbe\u4e5f<br/>label: 1<br/>Hierarchy: 2',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '53',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '54',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '55',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u7267\u6fd1\u9686\u53f2<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '56',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u672c\u57ce\u4fca\u660e<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '57',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '58',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u7247\u6850\u62f3<br/>label: 1<br/>Hierarchy: 2',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '59',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u6237\u6845\u52c7\u6b21<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '60',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '61',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '62',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '63',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '64',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '65',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '66',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '67',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '68',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '69',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '70',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '71',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '72',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '73',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '76',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '77',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '78',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '80',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '81',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '85',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '86',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '88',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '89',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '90',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '91',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '94',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '95',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '96',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '97',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '98',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '99',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '102',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '103',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '104',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '105',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '106',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '107',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '108',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '109',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '110',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '111',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '112',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '113',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '114',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '115',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '116',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '117',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '118',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '119',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '121',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '122',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '123',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '125',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '126',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '128',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '129',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '130',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '131',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '132',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '133',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '134',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '135',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '137',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '138',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '139',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '141',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '143',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '145',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '146',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '147',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '148',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '149',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '150',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '151',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '152',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '153',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '154',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '155',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '157',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '158',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '159',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '160',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '161',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '162',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '163',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '164',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '165',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '166',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '167',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '168',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '169',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '170',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '171',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '172',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '173',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '176',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '177',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '178',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '180',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '181',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '185',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '186',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '188',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '189',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '190',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '191',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '194',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '195',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '196',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '197',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '198',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '199',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '202',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '203',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '204',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '205',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '206',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '207',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '208',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '209',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '210',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '211',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '215',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '216',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '217',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '218',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '219',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '220',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '221',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '223',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '224',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '225',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '227',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '228',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '230',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '231',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '232',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u6749\u539f\u8bda<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '233',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u6850\u8c37\u5065\u592a<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            },
            {
              name: '234',
              fixed: false,
              symbolSize: 30,
              itemStyle: {
                color: '#87CEFA'
              },
              emphasis: {},
              blur: {},
              select: {},
              tooltip: {
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove|click',
                axisPointer: {
                  type: 'line'
                },
                showContent: true,
                alwaysShowContent: false,
                showDelay: 0,
                hideDelay: 100,
                enterable: false,
                confine: false,
                appendToBody: false,
                transitionDuration: 0.4,
                formatter: '<br/>Name: \u4f0a\u5d0e\u77ac<br/>label: 1<br/>Hierarchy: 3',
                textStyle: {
                  fontSize: 14
                },
                borderWidth: 0,
                padding: 5,
                order: 'seriesAsc'
              }
            }
          ]

        },
      nodeEmbeddingChartsSeries: {
        series: [
          {
            data: [
              [
                -6.9105939865112305,
                -2.5236706733703613
              ],
              [
                15.99852466583252,
                3.72902250289917
              ],
              [
                7.606411933898926,
                -0.017911618575453758
              ],
              [
                9.076478004455566,
                -7.3317341804504395
              ],
              [
                2.9361791610717773,
                -11.450322151184082
              ],
              [
                0.7405006289482117,
                -7.378413200378418
              ],
              [
                7.634803295135498,
                0.03853468596935272
              ],
              [
                3.03251314163208,
                -11.66761302947998
              ],
              [
                10.273222923278809,
                -7.6827392578125
              ],
              [
                3.458381652832031,
                -15.079184532165527
              ],
              [
                5.755165100097656,
                10.00374698638916
              ],
              [
                3.418287992477417,
                12.063331604003906
              ],
              [
                3.1974246501922607,
                -15.226696968078613
              ],
              [
                3.58406138420105,
                -15.292107582092285
              ],
              [
                0.48567765951156616,
                15.390438079833984
              ],
              [
                0.6395911574363708,
                16.399770736694336
              ],
              [
                7.673762321472168,
                -4.327245235443115
              ],
              [
                8.381529808044434,
                -4.104665279388428
              ],
              [
                -0.27791398763656616,
                -11.878549575805664
              ],
              [
                -3.225775957107544,
                -6.483657360076904
              ],
              [
                -2.4672179222106934,
                -7.721443176269531
              ],
              [
                11.846835136413574,
                2.346456527709961
              ],
              [
                11.999661445617676,
                -0.5573268532752991
              ],
              [
                11.943309783935547,
                -0.5671070218086243
              ],
              [
                -0.9667304158210754,
                -1.1796292066574097
              ],
              [
                -1.9007552862167358,
                -0.1854749321937561
              ],
              [
                -0.3133904039859772,
                8.265226364135742
              ],
              [
                0.20728032290935516,
                7.463217258453369
              ],
              [
                4.136183738708496,
                5.4939985275268555
              ],
              [
                3.4823124408721924,
                5.096444129943848
              ],
              [
                2.4312689304351807,
                4.813726425170898
              ],
              [
                1.7045505046844482,
                5.357239723205566
              ],
              [
                0.5543273687362671,
                5.4897284507751465
              ],
              [
                0.3290064334869385,
                3.380988359451294
              ],
              [
                -0.14861628413200378,
                2.8226497173309326
              ],
              [
                -3.583451509475708,
                -15.858092308044434
              ],
              [
                -2.0313880443573,
                -16.010549545288086
              ],
              [
                -7.100034236907959,
                4.444235324859619
              ],
              [
                -4.58556604385376,
                3.664285659790039
              ],
              [
                -5.3220038414001465,
                3.543361186981201
              ],
              [
                10.903454780578613,
                7.150726318359375
              ],
              [
                11.811675071716309,
                7.699830055236816
              ],
              [
                -6.109499454498291,
                -5.884044647216797
              ],
              [
                -0.6052025556564331,
                -5.140112400054932
              ],
              [
                11.245271682739258,
                -4.953197479248047
              ],
              [
                -8.485991477966309,
                -0.7461867928504944
              ],
              [
                -2.474165916442871,
                -4.607481002807617
              ],
              [
                9.329194068908691,
                -15.290014266967773
              ],
              [
                -3.816441535949707,
                11.801753044128418
              ],
              [
                -3.066528797149658,
                12.26095199584961
              ],
              [
                -2.2361435890197754,
                7.430786609649658
              ],
              [
                -0.7331991195678711,
                -10.759613037109375
              ],
              [
                6.062361717224121,
                5.27364444732666
              ],
              [
                15.869258880615234,
                -4.303802967071533
              ],
              [
                15.94825744628906,
                -5.537307262420654
              ],
              [
                7.475916385650635,
                12.298136711120605
              ],
              [
                5.635618209838867,
                11.997832298278809
              ],
              [
                -9.547830581665039,
                -2.294116497039795
              ],
              [
                -2.053053855895996,
                7.094634056091309
              ],
              [
                -12.033061981201172,
                -2.755096197128296
              ],
              [
                -15.566961288452148,
                3.5496599674224854
              ],
              [
                -4.022428035736084,
                -8.125923156738281
              ],
              [
                -13.477839469909668,
                3.814542293548584
              ],
              [
                -6.352077007293701,
                -11.42018985748291
              ],
              [
                -5.308426380157471,
                -12.107560157775879
              ],
              [
                -6.880714416503906,
                -13.064358711242676
              ],
              [
                -6.657676696777344,
                -11.062027931213379
              ],
              [
                -13.333053588867188,
                2.74878191947937
              ],
              [
                -5.527841567993164,
                -2.642221212387085
              ],
              [
                -5.237508296966553,
                -3.5236003398895264
              ],
              [
                -3.5214128494262695,
                8.162463188171387
              ],
              [
                -6.228408336639404,
                15.44259262084961
              ],
              [
                -6.228404998779297,
                12.92309284210205
              ],
              [
                -7.210513114929199,
                11.593649864196777
              ],
              [
                -8.478586196899414,
                -1.4283080101013184
              ],
              [
                -7.331367492675781,
                -1.9863625764846802
              ],
              [
                10.38663101196289,
                -7.946913242340088
              ],
              [
                11.430930137634277,
                -8.827932357788086
              ],
              [
                -0.6290290951728821,
                -15.40909481048584
              ],
              [
                -3.617286205291748,
                12.305805206298828
              ],
              [
                5.257837772369385,
                11.4624605178833
              ],
              [
                2.2799386978149414,
                12.628660202026367
              ],
              [
                -9.683884620666504,
                10.188921928405762
              ],
              [
                -8.489816665649414,
                6.207794666290283
              ],
              [
                0.675983726978302,
                15.361967086791992
              ],
              [
                -11.101426124572754,
                2.3271069526672363
              ],
              [
                0.0658070370554924,
                15.4734525680542
              ],
              [
                -7.531337261199951,
                -2.7558183670043945
              ],
              [
                3.4292352199554443,
                -16.513763427734375
              ],
              [
                -0.760094404220581,
                10.62953186035156
              ],
              [
                -0.7185184359550476,
                -10.49494743347168
              ],
              [
                -0.3957001864910126,
                -11.502093315124512
              ],
              [
                -1.9267507791519165,
                -7.1809492111206055
              ],
              [
                -8.560301780700684,
                1.2635937929153442
              ],
              [
                -2.502696990966797,
                -7.713924884796143
              ],
              [
                -4.052236557006836,
                7.3878278732299805
              ],
              [
                -2.216231346130371,
                -4.674962520599365
              ],
              [
                11.62209701538086,
                1.5714466571807861
              ],
              [
                -8.222575187683105,
                1.9120357036590576
              ],
              [
                16.62702941894531,
                -1.4313328266143799
              ],
              [
                11.130228996276855,
                0.7519943118095398
              ],
              [
                -2.2534685134887695,
                -1.4055571556091309
              ],
              [
                -2.795099973678589,
                5.00053071975708
              ],
              [
                -2.4856793880462646,
                -1.550413966178894
              ],
              [
                1.0711021423339844,
                8.416650772094727
              ],
              [
                -1.186713695526123,
                6.554091453552246
              ],
              [
                0.512600839138031,
                7.99207067489624
              ],
              [
                -3.2805867195129395,
                3.7328081130981445
              ],
              [
                -7.440758228302002,
                -3.760028123855591
              ],
              [
                3.91589617729187,
                6.0555195808410645
              ],
              [
                2.8338096141815186,
                4.210456848144531
              ],
              [
                3.322164297103882,
                3.534104585647583
              ],
              [
                3.8807730674743652,
                3.0546422004699707
              ],
              [
                -0.11991559714078903,
                5.677624225616455
              ],
              [
                4.890007019042969,
                2.6836886405944824
              ],
              [
                -0.1965329796075821,
                2.7225489616394043
              ],
              [
                -3.0131263732910156,
                -15.990422248840332
              ],
              [
                -2.287276029586792,
                -16.248802185058594
              ],
              [
                -6.9165358543396,
                4.628645420074463
              ],
              [
                -4.766879558563232,
                3.03662371635437
              ],
              [
                -5.064690589904785,
                3.828233003616333
              ],
              [
                11.564813613891602,
                7.110560894012451
              ],
              [
                11.797242164611816,
                6.685863018035889
              ],
              [
                -7.1127610206604,
                -7.60114860534668
              ],
              [
                -0.4129886329174042,
                -5.283546447753906
              ],
              [
                5.411964416503906,
                -6.835818290710449
              ],
              [
                -8.737493515014648,
                -0.7378652095794678
              ],
              [
                -7.136318683624268,
                -7.641050815582275
              ],
              [
                9.397391319274902,
                -15.26574993133545
              ],
              [
                -4.995609760284424,
                11.502241134643555
              ],
              [
                -3.814579725265503,
                14.139452934265137
              ],
              [
                -8.466590881347656,
                6.162023067474365
              ],
              [
                -2.1525800228118896,
                10.08690357208252
              ],
              [
                6.030123233795166,
                5.273636341094971
              ],
              [
                15.869770050048828,
                -4.344170093536377
              ],
              [
                7.962347507476807,
                -15.915489196777344
              ],
              [
                7.694749355316162,
                11.77988338470459
              ],
              [
                7.2418365478515625,
                10.996950149536133
              ],
              [
                -10.636073112487793,
                -1.0860989093780518
              ],
              [
                16.317930221557617,
                -3.121478319168091
              ],
              [
                -12.58298110961914,
                -3.1309728622436523
              ],
              [
                -15.683757781982422,
                3.4948477745056152
              ],
              [
                -5.205102443695068,
                -4.7159743309021
              ],
              [
                -13.397013664245605,
                2.779305934906006
              ],
              [
                -5.125906944274902,
                -11.29788589477539
              ],
              [
                -4.834447383880615,
                8.495318412780762
              ],
              [
                -5.011202335357666,
                -10.942893981933594
              ],
              [
                -6.337368011474609,
                -10.796698570251465
              ],
              [
                -14.116255760192871,
                4.507802486419678
              ],
              [
                -8.955008506774902,
                -4.980011463165283
              ],
              [
                -6.234572887420654,
                15.469305038452148
              ],
              [
                -9.877840995788574,
                10.354150772094727
              ],
              [
                -5.298913478851318,
                -3.245399475097656
              ],
              [
                -8.113080024719238,
                11.03284740447998
              ],
              [
                -7.334346771240234,
                12.237446784973145
              ],
              [
                -9.283095359802246,
                -3.189944267272949
              ],
              [
                -6.509318828582764,
                -1.6127601861953735
              ],
              [
                10.711627960205078,
                -7.731714248657227
              ],
              [
                7.113023281097412,
                -0.9844599962234497
              ],
              [
                -4.299985408782959,
                12.959327697753906
              ],
              [
                5.287857532501221,
                11.4209623336792
              ],
              [
                2.2841992378234863,
                12.635902404785156
              ],
              [
                -10.676610946655273,
                10.442163467407227
              ],
              [
                -2.4711127281188965,
                8.301165580749512
              ]
            ],
            itemStyle: {
              color: 'blue'
            },
            name: 'community 1',
            symbolSize: 5,
            type: 'scatter'
          },
          {
            data: [
              [
                1.7918727397918701,
                -0.5138983130455017
              ],
              [
                -11.343110084533691,
                -8.660737991333008
              ],
              [
                15.993107795715332,
                3.727585554122925
              ],
              [
                3.4036386013031006,
                -4.026341915130615
              ],
              [
                2.0688183307647705,
                -1.3450229167938232
              ],
              [
                1.5363727807998657,
                -2.164679765701294
              ],
              [
                3.5861754417419434,
                -1.256227970123291
              ],
              [
                1.7513905763626099,
                -0.48340457677841187
              ],
              [
                2.8413689136505127,
                -1.3486356735229492
              ],
              [
                3.755714178085327,
                -5.806485176086426
              ],
              [
                1.6962037086486816,
                -5.764194011688232
              ],
              [
                7.46090030670166,
                -6.776616096496582
              ],
              [
                2.8146281242370605,
                -9.057969093322754
              ],
              [
                3.4899888038635254,
                -2.9033758640289307
              ],
              [
                5.705534934997559,
                -4.266291618347168
              ],
              [
                3.9604756832122803,
                -3.23746395111084
              ],
              [
                3.1427149772644043,
                -8.361021041870117
              ],
              [
                3.387099504470825,
                -7.6783246994018555
              ],
              [
                3.3788344860076904,
                -6.604772567749023
              ],
              [
                1.2153897285461426,
                -4.910694122314453
              ],
              [
                1.7861381769180298,
                -6.126123428344727
              ],
              [
                7.6270647048950195,
                -4.352041244506836
              ],
              [
                6.107998371124268,
                -9.323894500732422
              ],
              [
                1.2390174865722656,
                -6.284456729888916
              ],
              [
                7.10211181640625,
                -11.833094596862793
              ],
              [
                7.525331497192383,
                -10.570230484008789
              ],
              [
                5.101999282836914,
                -3.100287437438965
              ],
              [
                5.15913200378418,
                -3.3025684356689453
              ],
              [
                7.206076145172119,
                -10.018990516662598
              ],
              [
                6.382716655731201,
                -10.344210624694824
              ],
              [
                6.424560546875,
                -9.689144134521484
              ]
            ],
            itemStyle: {
              color: 'red'
            },
            name: 'community 2',
            symbolSize: 5,
            type: 'scatter'
          }
        ],
        title: {
          text: 'Node Embeddings Visualization'
        },
        xAxis: [
          {
            max: 17.62702941894531,
            min: -16.683757781982422,
            type: 'value'
          }
        ],
        yAxis: [
          {
            max: 17.399770736694336,
            min: -17.513763427734375,
            type: 'value'
          }
        ]
      },
      subGraphSeries: {
        nodes: [
          {
            name: '2',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u94dc\u5c9b\u5e7f\u6d77<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '4',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u8c6a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '7',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u725b\u5c71<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '8',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#7FFFD4'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '13',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '14',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fde\u6cfd\u7460\u52a0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '16',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u5b66<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '18',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7530\u6751\u5fe0\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '21',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '22',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6797\u7530\u60e0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '24',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '29',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u83c5\u7530\u548c\u5fd7<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '31',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '33',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#DC143C'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u591a\u6469\u96c4<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '36',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '37',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#DC143C'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6cf7\u8c37\u6e90\u6cbb<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '40',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e9a\u4e45\u6d25\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '41',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u9e6b\u5c3e\u4e61\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '42',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u955d\u6728\u65cb\u98ce\u96c4<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '44',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#DC143C'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u79c0\u4eba<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '45',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '48',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8f6e\u5c9b\u77e2\u5c9b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '49',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7b52\u672c\u5c06\u6cbb<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '52',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#7FFFD4'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5c71\u5d0e\u8fbe\u4e5f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '55',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7267\u6fd1\u9686\u53f2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '56',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u672c\u57ce\u4fca\u660e<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '58',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#7FFFD4'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7247\u6850\u62f3<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '59',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6237\u6845\u52c7\u6b21<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '232',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6749\u539f\u8bda<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '233',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6850\u8c37\u5065\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '234',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4f0a\u5d0e\u77ac<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          }
        ],
        links: [
          {
            source: '2',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '2',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          }
        ]
      },
      minedCommunityGraphSeries:
      {
        nodes: [
          {
            name: '1',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '2',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u94dc\u5c9b\u5e7f\u6d77<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '3',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f\u7684\u6069\u4eba<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '4',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u8c6a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '6',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '7',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u725b\u5c71<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '8',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '9',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '10',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa\u7684\u540c\u5b66<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '11',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '12',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u521d\u604b<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '13',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '14',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fde\u6cfd\u7460\u52a0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '15',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa\u7684\u5f1f\u5f1f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '16',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u5b66<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '18',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7530\u6751\u5fe0\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '19',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '21',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '22',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6797\u7530\u60e0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '23',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1\u7684\u5973\u53cb<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '24',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '25',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '26',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '27',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b\u7684\u5802\u5144<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '28',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b\u7684\u53d1\u5c0f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '29',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u83c5\u7530\u548c\u5fd7<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '30',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '31',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '32',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '33',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u591a\u6469\u96c4<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '34',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '35',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '36',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '37',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6cf7\u8c37\u6e90\u6cbb<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '38',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '39',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '40',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e9a\u4e45\u6d25\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '41',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u9e6b\u5c3e\u4e61\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '42',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u955d\u6728\u65cb\u98ce\u96c4<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '43',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '44',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u79c0\u4eba<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '45',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '46',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '47',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '48',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8f6e\u5c9b\u77e2\u5c9b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '49',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7b52\u672c\u5c06\u6cbb<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '50',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '51',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '52',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5c71\u5d0e\u8fbe\u4e5f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '53',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '54',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '55',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7267\u6fd1\u9686\u53f2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '56',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u672c\u57ce\u4fca\u660e<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '57',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '58',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7247\u6850\u62f3<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '59',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6237\u6845\u52c7\u6b21<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '60',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '61',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '62',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '63',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '64',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '65',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '66',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '67',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '68',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '69',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '70',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '71',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '72',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '73',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '76',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '77',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '78',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '80',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '81',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '85',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '86',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '88',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '89',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '90',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '91',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '94',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '95',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '96',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '97',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '98',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '99',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '102',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '103',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '104',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '105',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '106',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '107',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '108',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '109',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '110',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '111',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '112',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '113',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '114',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '115',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '116',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '117',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '118',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '119',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '121',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '122',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '123',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '125',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '126',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '128',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '129',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '130',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '131',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '132',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '133',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '134',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '135',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '137',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '138',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '139',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '141',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '143',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '145',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '146',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '147',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '148',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '149',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '150',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '151',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '152',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '153',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '154',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '155',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '157',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '158',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '159',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '160',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '161',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '162',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '163',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '164',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '165',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '166',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '167',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '168',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '169',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '170',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '171',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '172',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '173',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '176',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '177',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '178',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '180',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '181',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '185',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '186',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '188',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '189',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '190',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '191',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '194',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '195',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '196',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '197',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '198',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '199',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '202',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '203',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '204',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '205',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '206',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '207',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '208',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '209',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '210',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '211',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '215',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '216',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '217',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '218',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '219',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '220',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '221',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '223',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '224',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '225',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '227',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '228',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '230',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '231',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u666e\u901a\u5b66\u751f<br/>label: 0<br/>Hierarchy: 0',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '232',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6749\u539f\u8bda<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '233',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6850\u8c37\u5065\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '234',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4f0a\u5d0e\u77ac<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          }
        ],
        links: [
          {
            source: '1',
            target: '111',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '2',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '2',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '3',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '6',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '6',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '9',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '9',
            target: '119',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '168',
            target: '122',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '118',
            target: '141',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '128',
            target: '145',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '138',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '118',
            target: '159',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '10',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '11',
            target: '122',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '11',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '12',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '114',
            target: '131',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '51',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '114',
            target: '95',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '117',
            target: '98',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '119',
            target: '121',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '15',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '19',
            target: '119',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '88',
            target: '115',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '122',
            target: '35',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '122',
            target: '38',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '122',
            target: '43',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '23',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '25',
            target: '125',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '125',
            target: '26',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '25',
            target: '26',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '26',
            target: '126',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '126',
            target: '30',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '26',
            target: '30',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '30',
            target: '130',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '30',
            target: '130',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '130',
            target: '32',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '32',
            target: '132',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '132',
            target: '130',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '34',
            target: '134',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '34',
            target: '35',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '135',
            target: '134',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '35',
            target: '135',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '35',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '135',
            target: '137',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '137',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '38',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '137',
            target: '138',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '38',
            target: '138',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '38',
            target: '39',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '138',
            target: '139',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '39',
            target: '139',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '139',
            target: '43',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '139',
            target: '143',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '43',
            target: '143',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '43',
            target: '46',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '143',
            target: '146',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '46',
            target: '146',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '46',
            target: '47',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '146',
            target: '147',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '47',
            target: '147',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '150',
            target: '147',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '50',
            target: '47',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '50',
            target: '150',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '150',
            target: '151',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '50',
            target: '51',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '51',
            target: '151',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '151',
            target: '153',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '53',
            target: '51',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '53',
            target: '153',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '154',
            target: '153',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '53',
            target: '54',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '54',
            target: '154',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '154',
            target: '157',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '54',
            target: '57',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '57',
            target: '157',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '157',
            target: '160',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '57',
            target: '60',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '60',
            target: '160',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '160',
            target: '161',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '60',
            target: '61',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '61',
            target: '161',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '161',
            target: '162',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '61',
            target: '62',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '62',
            target: '162',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '162',
            target: '163',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '62',
            target: '63',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '63',
            target: '163',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '163',
            target: '164',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '63',
            target: '64',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '64',
            target: '164',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '164',
            target: '165',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '64',
            target: '65',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '65',
            target: '165',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '66',
            target: '65',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '66',
            target: '166',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '166',
            target: '167',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '67',
            target: '167',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '67',
            target: '68',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '167',
            target: '168',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '68',
            target: '168',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '69',
            target: '70',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '169',
            target: '170',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '69',
            target: '169',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '70',
            target: '170',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '70',
            target: '171',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '170',
            target: '171',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '71',
            target: '171',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '72',
            target: '73',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '172',
            target: '173',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '72',
            target: '172',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '73',
            target: '173',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '76',
            target: '176',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '76',
            target: '77',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '176',
            target: '177',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '177',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '78',
            target: '178',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '80',
            target: '180',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '81',
            target: '181',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '81',
            target: '77',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '181',
            target: '177',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '85',
            target: '185',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '86',
            target: '186',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '88',
            target: '188',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '88',
            target: '86',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '188',
            target: '186',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '89',
            target: '189',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '90',
            target: '190',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '91',
            target: '191',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '90',
            target: '89',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '190',
            target: '188',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '94',
            target: '194',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '95',
            target: '195',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '195',
            target: '196',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '94',
            target: '95',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '96',
            target: '196',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '196',
            target: '197',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '96',
            target: '97',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '97',
            target: '197',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '98',
            target: '198',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '199',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '97',
            target: '99',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '199',
            target: '197',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '102',
            target: '202',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '103',
            target: '203',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '104',
            target: '204',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '105',
            target: '210',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '105',
            target: '102',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '210',
            target: '103',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '106',
            target: '209',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '107',
            target: '106',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '107',
            target: '208',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '208',
            target: '206',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '108',
            target: '209',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '109',
            target: '206',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '109',
            target: '209',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '110',
            target: '205',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '111',
            target: '211',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '112',
            target: '217',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '110',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '111',
            target: '217',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '216',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '114',
            target: '215',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '115',
            target: '114',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '218',
            target: '113',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '115',
            target: '218',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '116',
            target: '219',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '116',
            target: '218',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '115',
            target: '219',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '117',
            target: '220',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '220',
            target: '221',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '117',
            target: '118',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '118',
            target: '221',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '119',
            target: '223',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '121',
            target: '223',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '122',
            target: '224',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '123',
            target: '225',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '125',
            target: '227',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '126',
            target: '228',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '128',
            target: '230',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '129',
            target: '231',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '80',
            target: '117',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '27',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '28',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '30',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '32',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '39',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '141',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '57',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '88',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '102',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '105',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '110',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '121',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '158',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '131',
            target: '164',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '95',
            target: '178',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '95',
            target: '195',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '95',
            target: '197',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '97',
            target: '227',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '39',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '204',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '146',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '147',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '153',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '158',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '159',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '173',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '178',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '185',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '196',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '107',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '112',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '77',
            target: '121',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '88',
            target: '123',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '90',
            target: '138',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '91',
            target: '157',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '34',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '35',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '35',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '38',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '141',
            target: '145',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '141',
            target: '148',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '43',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '122',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '231',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '152',
            target: '158',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '89',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '99',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '145',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '152',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '186',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '207',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '113',
            target: '231',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '65',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '89',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '97',
            target: '99',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '145',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '152',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '186',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '207',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '99',
            target: '231',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '54',
            target: '155',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '145',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '148',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '149',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '164',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '171',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '195',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '155',
            target: '197',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '1',
            target: '118',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '1',
            target: '133',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          }
        ]
      },
      centralityGraphsSeries1: {
        links: [
          {
            source: '2',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '2',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          }
        ],
        nodes: [
          {
            name: '2',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u94dc\u5c9b\u5e7f\u6d77<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '4',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u8c6a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '7',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u725b\u5c71<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '8',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#7FFFD4'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '13',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '14',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fde\u6cfd\u7460\u52a0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '16',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u5b66<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '18',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7530\u6751\u5fe0\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '21',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '22',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6797\u7530\u60e0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '24',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '29',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u83c5\u7530\u548c\u5fd7<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '31',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '33',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#DC143C'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u591a\u6469\u96c4<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '36',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '37',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#DC143C'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6cf7\u8c37\u6e90\u6cbb<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '40',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e9a\u4e45\u6d25\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '41',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u9e6b\u5c3e\u4e61\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '42',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u955d\u6728\u65cb\u98ce\u96c4<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '44',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#DC143C'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u79c0\u4eba<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '45',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '48',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8f6e\u5c9b\u77e2\u5c9b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '49',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7b52\u672c\u5c06\u6cbb<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '52',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#7FFFD4'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5c71\u5d0e\u8fbe\u4e5f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '55',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7267\u6fd1\u9686\u53f2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '56',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u672c\u57ce\u4fca\u660e<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '58',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#7FFFD4'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7247\u6850\u62f3<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '59',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6237\u6845\u52c7\u6b21<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '232',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6749\u539f\u8bda<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '233',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6850\u8c37\u5065\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '234',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4f0a\u5d0e\u77ac<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          }
        ],
        links_b: [
          {
            source: '2',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '2',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          }
        ],
        nodes_b: [
          {
            name: '2',
            fixed: false,
            symbolSize: 25,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u94dc\u5c9b\u5e7f\u6d77<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '4',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u8c6a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '7',
            fixed: false,
            symbolSize: 21,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u725b\u5c71<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '8',
            fixed: false,
            symbolSize: 42,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '13',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '14',
            fixed: false,
            symbolSize: 28,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fde\u6cfd\u7460\u52a0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '16',
            fixed: false,
            symbolSize: 33,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u5b66<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '18',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7530\u6751\u5fe0\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '21',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '22',
            fixed: false,
            symbolSize: 31,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6797\u7530\u60e0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '24',
            fixed: false,
            symbolSize: 34,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '29',
            fixed: false,
            symbolSize: 22,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u83c5\u7530\u548c\u5fd7<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '31',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '33',
            fixed: false,
            symbolSize: 44,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u591a\u6469\u96c4<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '36',
            fixed: false,
            symbolSize: 22,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '37',
            fixed: false,
            symbolSize: 44,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6cf7\u8c37\u6e90\u6cbb<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '40',
            fixed: false,
            symbolSize: 22,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e9a\u4e45\u6d25\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '41',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u9e6b\u5c3e\u4e61\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '42',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u955d\u6728\u65cb\u98ce\u96c4<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '44',
            fixed: false,
            symbolSize: 44,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u79c0\u4eba<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '45',
            fixed: false,
            symbolSize: 32,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '48',
            fixed: false,
            symbolSize: 26,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8f6e\u5c9b\u77e2\u5c9b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '49',
            fixed: false,
            symbolSize: 20,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7b52\u672c\u5c06\u6cbb<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '52',
            fixed: false,
            symbolSize: 39,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5c71\u5d0e\u8fbe\u4e5f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '55',
            fixed: false,
            symbolSize: 20,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7267\u6fd1\u9686\u53f2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '56',
            fixed: false,
            symbolSize: 14,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u672c\u57ce\u4fca\u660e<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '58',
            fixed: false,
            symbolSize: 39,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7247\u6850\u62f3<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '59',
            fixed: false,
            symbolSize: 26,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6237\u6845\u52c7\u6b21<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '232',
            fixed: false,
            symbolSize: 20,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6749\u539f\u8bda<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '233',
            fixed: false,
            symbolSize: 23,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6850\u8c37\u5065\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '234',
            fixed: false,
            symbolSize: 27,
            itemStyle: {
              color: '#FFA07A'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4f0a\u5d0e\u77ac<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          }
        ],
        links_c: [
          {
            source: '2',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '2',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '4',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '7',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '8',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '13',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '21',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '14',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '18',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '16',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '22',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '24',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '31',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '42',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '45',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '24',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '29',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '31',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '36',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '40',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '41',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '42',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '45',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '48',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '22',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '33',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '52',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '55',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '44',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '33',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '37',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '52',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '44',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '232',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '55',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '233',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '56',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '232',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '233',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '58',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '234',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '2',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '4',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '8',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '7',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '13',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '14',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '18',
            target: '21',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '59',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '37',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '49',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '234',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          },
          {
            source: '58',
            target: '16',
            emphasis: {},
            blur: {},
            select: {},
            ignoreForceLayout: false
          }
        ],
        nodes_c: [
          {
            name: '2',
            fixed: false,
            symbolSize: 14,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u94dc\u5c9b\u5e7f\u6d77<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '4',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u8c6a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '7',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u725b\u5c71<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '8',
            fixed: false,
            symbolSize: 28,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fb0\u5ddd\u65f6\u751f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '13',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '14',
            fixed: false,
            symbolSize: 12,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8fde\u6cfd\u7460\u52a0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '16',
            fixed: false,
            symbolSize: 20,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e09\u4e0a\u5b66<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '18',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7530\u6751\u5fe0\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '21',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '22',
            fixed: false,
            symbolSize: 18,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6797\u7530\u60e0<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '24',
            fixed: false,
            symbolSize: 14,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '29',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u83c5\u7530\u548c\u5fd7<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '31',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5343\u7530\u76f4\u7eaa<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '33',
            fixed: false,
            symbolSize: 19,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u82b9\u6cfd\u591a\u6469\u96c4<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '36',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u6253\u624b1<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '37',
            fixed: false,
            symbolSize: 24,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6cf7\u8c37\u6e90\u6cbb<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '40',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4e9a\u4e45\u6d25\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '41',
            fixed: false,
            symbolSize: 14,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u9e6b\u5c3e\u4e61\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '42',
            fixed: false,
            symbolSize: 11,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u955d\u6728\u65cb\u98ce\u96c4<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '44',
            fixed: false,
            symbolSize: 21,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5742\u4e1c\u79c0\u4eba<br/>label: 1<br/>Hierarchy: 1',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '45',
            fixed: false,
            symbolSize: 12,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5f3a\u7f57\u5f7b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '48',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u8f6e\u5c9b\u77e2\u5c9b<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '49',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7b52\u672c\u5c06\u6cbb<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '52',
            fixed: false,
            symbolSize: 22,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u5c71\u5d0e\u8fbe\u4e5f<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '55',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7267\u6fd1\u9686\u53f2<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '56',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u672c\u57ce\u4fca\u660e<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '58',
            fixed: false,
            symbolSize: 30,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u7247\u6850\u62f3<br/>label: 1<br/>Hierarchy: 2',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '59',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6237\u6845\u52c7\u6b21<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '232',
            fixed: false,
            symbolSize: 10,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6749\u539f\u8bda<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '233',
            fixed: false,
            symbolSize: 12,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u6850\u8c37\u5065\u592a<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          },
          {
            name: '234',
            fixed: false,
            symbolSize: 14,
            itemStyle: {
              color: '#87CEFA'
            },
            emphasis: {},
            blur: {},
            select: {},
            tooltip: {
              show: true,
              trigger: 'item',
              triggerOn: 'mousemove|click',
              axisPointer: {
                type: 'line'
              },
              showContent: true,
              alwaysShowContent: false,
              showDelay: 0,
              hideDelay: 100,
              enterable: false,
              confine: false,
              appendToBody: false,
              transitionDuration: 0.4,
              formatter: '<br/>Name: \u4f0a\u5d0e\u77ac<br/>label: 1<br/>Hierarchy: 3',
              textStyle: {
                fontSize: 14
              },
              borderWidth: 0,
              padding: 5,
              order: 'seriesAsc'
            }
          }
        ]
      }
    }
  },
  mounted () {
    this.getUploadAction(1)
  },
  methods: {
    handleUploadAttributes (response) {
      if (response) {
        this.uploadNumber = this.uploadNumber + 1
        console.log(this.uploadNumber)
      } else {
        console.log('2222')
      }
    },
    handleUploadEdgelist (response) {
      if (response) {
        this.uploadNumber = this.uploadNumber + 1
        console.log(this.uploadNumber)
      } else {
        console.log('2222')
      }
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
          this.upAttributesList = []
          this.upEdgeList = []
        })
        .catch(_ => {})
    },
    skip_one (event) {
      event.stopPropagation()
      this.nameNumber = 1
      this.getUploadAction(this.namNumber)
    },
    skip_two (event) {
      event.stopPropagation()
      this.nameNumber = 2
    },
    skip_three (event) {
      event.stopPropagation()
      this.nameNumber = 3
    },
    skip_four (event) {
      event.stopPropagation()
      this.nameNumber = 4
    },
    skip_five (event) {
      event.stopPropagation()
      this.nameNumber = 5
    },
    getUploadAction (nameNumber) {
      switch (nameNumber) {
        case 1:
        // this.actionPath = 'http://localhost:5000/globalGraphSeries'
          if (this.uploadNumber % 2 !== 0) {
            this.$message.error('请先上传两个txt文件')
            this.upAttributesList = []
            this.upEdgeList = []
            return
          }
          this.drawer = false
          this.loading = true
          axios.post('http://localhost:5000/globalGraphSeries').then((response) => {
          // this.anticipatedData = response.data
            console.log('后端返回的数据：', response.data.links)
            this.globalGraphSeries = response.data
            console.log('后端返回的数据1：', this.globalGraphSeries)
            this.loading = false
            this.uploadNumber = 0
            this.upAttributesList = []
            this.upEdgeList = []
          }).catch((err) => {
            console.log('上传过程中发生错误：', err)
            this.loading = false
            this.uploadNumber = 0
          })
          break
        case 2:
        // this.actionPath = 'http://localhost:5000/minedCommunityGraphSeries'
          if (this.uploadNumber !== 2) {
            this.$message.error('请先上传两个txt文件')
            this.upAttributesList = []
            this.upEdgeList = []
            return
          }
          this.drawer = false
          this.loading = true
          axios.post('http://localhost:5000/minedCommunityGraphSeries').then((response) => {
          // this.anticipatedData = response.data
            console.log('后端返回的数据：', response.data)
            this.minedCommunityGraphSeries = response.data
            this.loading = false
            this.uploadNumber = 0
            this.upAttributesList = []
            this.upEdgeList = []
          }).catch((err) => {
            console.log('上传过程中发生错误：', err)
            this.loading = false
            this.uploadNumber = 0
          })
          break
        case 3:
        // this.actionPath = 'http://localhost:5000/nodeEmbeddingChartsSeries'
          if (this.uploadNumber !== 2) {
            this.$message.error('请先上传两个txt文件')

            return
          }
          this.drawer = false
          this.loading = true
          axios.post('http://localhost:5000/nodeEmbeddingChartsSeries').then((response) => {
          // this.anticipatedData = response.data
          // this.nodeEmbeddingChartsSeries = response.data.series
            console.log('后端返回的数据：', response.data)
            this.nodeEmbeddingChartsSeries = response.data
            this.loading = false
            this.uploadNumber = 0
            this.upAttributesList = []
            this.upEdgeList = []
          }).catch((err) => {
            console.log('上传过程中发生错误：', err)
            this.loading = false
            this.uploadNumber = 0
          })
          break
        case 4:
          if (this.uploadNumber !== 2) {
            this.$message.error('请先上传两个txt文件')
            this.upAttributesList = []
            this.upEdgeList = []
            return
          }
          this.drawer = false
          this.loading = true
          // this.actionPath = 'http://localhost:5000/subGraphSeries'
          axios.post('http://localhost:5000/subGraphSeries').then((response) => {
          // this.anticipatedData = response.data
            console.log('后端返回的数据：', response.data)
            this.subGraphSeries = response.data
            this.loading = false
            this.uploadNumber = 0
            this.upAttributesList = []
            this.upEdgeList = []
          }).catch((err) => {
            console.log('上传过程中发生错误：', err)
            this.loading = false
            this.uploadNumber = 0
          })
          break
        case 5:
          if (this.uploadNumber !== 2) {
            this.$message.error('请先上传两个txt文件')
            this.upAttributesList = []
            this.upEdgeList = []
            return
          }
          this.drawer = false
          this.loading = true
          // this.actionPath = 'http://localhost:5000/centralityGraphsSeries1'
          axios.post('http://localhost:5000/centralityGraphsSeries1').then((response) => {
          // this.anticipatedData = response.data
            console.log('后端返回的数据：', response.data)
            this.centralityGraphsSeries1 = response.data
            this.loading = false
            this.uploadNumber = 0
            this.upAttributesList = []
            this.upEdgeList = []
          }).catch((err) => {
            console.log('上传过程中发生错误：', err)
            this.loading = false
            this.uploadNumber = 0
          })
          break
      }
    }
  }
}
</script>

<style lang="less" scoped>
.page-navigation{
  min-height: 100%;
    box-sizing: border-box;
    margin-left: 10px;
    background-color: #F8F8FF;
    .active{
      color: #00BFFF
    }
}
.page-container {
    min-height: 100%;
    box-sizing: border-box;
    margin-left: 10px;
}
.el-steps {
  margin-top: 0px;
    margin-bottom: 20px;
}
.upload-demo {
  margin-left: 45px;
}
</style>

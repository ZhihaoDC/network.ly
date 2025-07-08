<template> 
  <div class="parent_container">
    
    <!-- <b-form-group id="input-communityColor" label="Color de la comunidad" label-for="input-communityColor">
      <b-form-input type="color" v-model="communityColor" @input="updateCommunityColor()" @blur="updateEdgesColor()"></b-form-input>
    </b-form-group> -->

    <div id="container" ref="cy">
    </div>
  </div>
</template>

<script>
import cytoscape from "cytoscape";
import fcose from "cytoscape-fcose";

export default {
  name: "PlotNetwork",
  props:['isNewExperiment', 'visualizationParameters'],
  data: function() {
    return {
      experiment: this.$store.getters['experiment/getExperiment'], 
      community_detection_methods: ["Girvan-Newman", "Louvain"]
    }
  },
  emits: ['animation_finished'],
  watch:{
    visualizationParameters: {
      handler(newData){
        this.animation_finished = false
        var layoutOptions = this.getLayoutOptions(newData)
        this.cy.layout(layoutOptions).run();
      }, deep: true
    }
  },
  mounted() {
    let self = this
    cytoscape.use(fcose);

    this.cy = cytoscape({
      container: this.$refs.cy, // container to render in
      //set node and edges color based on node properties
      wheelSensitivity: 0.2,
      hideEdgesOnViewport: true,
      style: [
        {
          selector: "node",
          style: {
            label: "data(name)",
            height: "data(size)",
            width: "data(size)",
            "text-valign": "center",
            "background-color": (node) => node.data("background_color") ? node.data("background_color") : "#5CF",
            "text-outline-color": (node) => node.data("background_color") ? node.data("background_color") : "#fff",
            "text-outline-width": 2,
            "font-size": "data(font_size)",
            "color": (node) => node.data("background_color") ? this.contrast(node.data("background_color")) : "#000"
          },
        },
        {
          selector: "node:selected",
          style: {
            label: "data(name)",
            height: "data(size)",
            width: "data(size)",
            "text-valign": "center",
            "background-color": 
              function(node){
                if (node.data("background_color")){return node.data("background_color")}
                else {return "#5CF"}         
              },
            "text-outline-color": 
              function(){
                if (!(self.isCommunityDetection)){ return "#999999"}
                else {return "#999999"}
              },
            "text-outline-width": 7,
            "font-size": "data(font_size)"
          },
        },
        {
          selector: "edge",
          style: {
            visibility: "hidden",
            width: 0.5,
            "line-color": function(edge){
              if (self.isCommunityDetection){
                //take the color of highest degree node ('source' or 'target' node)
                if (cy.$id(edge.data("source")).data("degree") > cy.$id(edge.data("target")).data("degree")){
                  return cy.$id(edge.data("source")).data("background_color")
                }else{
                  return cy.$id(edge.data("target")).data("background_color")
                }
              }else{
                return "#666"
              }
            }
          },
        },
      ]
    });

    //define local variable
    let cy = this.cy

    
    //read graph from json
    cy.json(this.experiment.network_json);

    
    //define layout
    var layout_options = {
        name: "fcose",

        // 'draft', 'default' or 'proof'
        // - "draft" only applies spectral layout
        // - "default" improves the quality with incremental layout (fast cooling rate)
        // - "proof" improves the quality with incremental layout (slow cooling rate)
        quality: "default",
        
        // if this is set to false, then quality option must be "proof"
        randomize: self.isNewExperiment, // Use random node positions at beginning of layout. If this is set to false, then quality option must be "proof"

        animate: self.isNewExperiment, // Whether or not to animate the layout
        
        animationDuration: 3000, // Duration of animation in ms, if enabled
        
        animationEasing: 'ease-in-out', // Easing of animation, if enabled
        
        fit: true, // Fit the viewport to the repositioned nodes
        
        padding: 10, // Padding around layout
        
        nodeDimensionsIncludeLabels: true, // Whether to include labels in node dimensions. Valid in "proof" quality
        
        uniformNodeDimensions: true, // Whether or not simple nodes (non-compound nodes) are of uniform dimensions
        
        packComponents: true, // Whether to pack disconnected components - cytoscape-layout-utilities extension should be registered and initialized
        
        step: "all", // Layout step - all, transformed, enforced, cose - for debug purpose only


        /* spectral layout options */

        samplingType: true, // False for random, true for greedy sampling
        
        sampleSize: 25, // Sample size to construct distance matrix
        
        nodeSeparation: self.visualizationParameters.nodeSeparation, // Separation amount between nodes

        piTol: 0.0000001, // Power iteration tolerance

        /* incremental layout options */

        nodeRepulsion: 10000,// Node repulsion (non overlapping) multiplier

        // Ideal edge (non nested) length
        idealEdgeLength: function(edge){
          if (self.isCommunityDetection){
            if (cy.$id(edge.data().source).data().community === cy.$id(edge.data().target).data().community){
              return 50 * (1 - self.visualizationParameters.gravity) + (self.visualizationParameters.nodeSeparation / 1000)
            }else{
              return self.visualizationParameters.communitySeparation
            }
          }else{
            return null
          }
        },
        
        edgeElasticity: 0.45, // Divisor to compute edge forces
        
        nestingFactor: 0.1, // Nesting factor (multiplier) to compute ideal edge length for nested edges
        
        numIter: 2500, // Maximum number of iterations to perform - this is a suggested value and might be adjusted by the algorithm as required
      
        tile: true,  // For enabling tiling
        
        tilingPaddingVertical: 10, // Represents the amount of the vertical space to put between the zero degree members during the tiling operation(can also be a function)
        
        tilingPaddingHorizontal: 10, // Represents the amount of the horizontal space to put between the zero degree members during the tiling operation(can also be a function)
        
        gravity: self.visualizationParameters.gravity, // Gravity force (constant)
        
        gravityRangeCompound: 1.5, // Gravity range (constant) for compounds
        
        gravityCompound: 1.0, // Gravity force (constant) for compounds

        gravityRange: 3, // Gravity range (constant)
        
        initialEnergyOnIncremental: 0.3, // Initial cooling factor for incremental layout

        /* constraint options */

        // Fix desired nodes to predefined positions
        // [{nodeId: 'n1', position: {x: 100, y: 200}}, {...}]
        fixedNodeConstraint: undefined,
        // Align desired nodes in vertical/horizontal direction
        // {vertical: [['n1', 'n2'], [...]], horizontal: [['n2', 'n4'], [...]]}
        alignmentConstraint: undefined,
        // Place two nodes relatively in vertical/horizontal direction
        // [{top: 'n1', bottom: 'n2', gap: 100}, {left: 'n3', right: 'n4', gap: 75}, {...}]
        relativePlacementConstraint: undefined,

        /* layout event callbacks */
        ready: function() {
        }, // on layoutready
        stop: function () { // on layoutstop
          //set edges visible only when animation has stopped (for performance enhancements)
          cy.style().selector("edge").style("visibility", "visible").update();
          cy.nodes().unselect();
          self.animation_finished = true
          self.updateNetworkStatus()
          self.$emit('ready')
        },
        
      };

    //Run layout
    var layout = cy.layout(layout_options);
    layout.run();
    this.cy = cy;
    cy.animated();
    cy.selectionType('additive')

    //define events
    cy.on('click', 'node', (event) =>{
      
      var clickedNode = event.target
      
      if (this.isCommunityDetection){
        var community = clickedNode.data('community')
        var communityNodes = cy.nodes().filter(element=> {
          return (element.data('community') === community && element.id() != clickedNode.id())
        })
        cy.nodes().unselect()
        communityNodes.select()
      }
      else {clickedNode.select()
            clickedNode.grabify()}

      var communityColor = this.rgb_to_hex(clickedNode.style('background-color'))
      this.$emit('setSelectedColor', communityColor)
    })

    cy.on('dblclick', 'node', event=>{
      var clickedNode = event.target
      cy.nodes().unselect()
      clickedNode.select()
    })


  },

  methods:{
    updateJson(){
      let cy = this.cy
      
      let unselectedNodes = cy.nodes(':selected')
      cy.nodes().lock() //preserve json position
      cy.nodes().unselect()

      let new_json = cy.json();
      delete new_json.style //dont overwrite current style (colors)
      this.$store.commit('experiment/setNetwork', new_json);

      cy.nodes().unlock() //for visualization
      unselectedNodes.select()
    },

    updateThumbnail(){
      const options = {'scale': 0.15, 'output':'base64'}
      const thumbnail = this.cy.png(options)
      this.$store.commit('experiment/setThumbnail', thumbnail)

    },

    updateNetworkStatus(){
      this.updateJson()
      this.updateThumbnail()
    },

    exportNetwork(){
      this.updateNetworkStatus()
      this.$emit("network-exported")
    },
    
    getLayoutOptions(visualizationParameters){
      let cy = this.cy
      let self = this
      var layoutOptions = {
        name: "fcose",
        quality: "default",
        randomize: false,
        animate: true,
        animationDuration: 1000,
        animationEasing: 'ease-in-out',
        fit: false,
        padding: 10, 
        nodeDimensionsIncludeLabels: true,
        uniformNodeDimensions: true,
        packComponents: true,
        step: "cose",

        /* spectral layout options */
        samplingType: true, 
        sampleSize: 25,
        nodeSeparation: visualizationParameters.nodeSeparation, 
        piTol: 0.0000001, 
        /* incremental layout options */
        nodeRepulsion: 6000,

        // Ideal edge (non nested) length
        idealEdgeLength: function(edge){
          if (self.isCommunityDetection){
            if (cy.$id(edge.data().source).data().community === cy.$id(edge.data().target).data().community){
              return 50
            }else{
              return visualizationParameters.communitySeparation 
            }
          }else{
            return 150
          }
        },
        
        edgeElasticity: 0.45, 
        nestingFactor: 0.1, 
        numIter: 250, 
        tile: true,  
        tilingPaddingVertical: 10, 
        tilingPaddingHorizontal: 10, 
        gravity: visualizationParameters.gravity, 
        gravityRangeCompound: 1.5, 
        gravityCompound: 1.0, 
        gravityRange: 3,
        initialEnergyOnIncremental: 0.3, 

        /* layout event callbacks */
        ready: function() {
        }, // on layoutready
        stop: function () { // on layoutstop
          //set edges visible only when animation has stopped (for performance enhancements) 
          cy.style().selector("edge").style("visibility", "visible").update();
          self.animation_finished = true
          self.$emit('ready')
        },

        
      };
      return layoutOptions
    },

    changeCommunityColor(new_color){
      var color = new_color
      var fontColor = this.contrast(color)

      var selectedNodes = this.cy.nodes(':selected');

      selectedNodes.style('background-color', color)
      selectedNodes.style('text-outline-color', color)
      selectedNodes.style('color', fontColor)
      selectedNodes.data('background_color', color)
    },

    updateEdgesColor(){
      let self = this
      var selectedNodes = this.cy.nodes(':selected');
      var color = selectedNodes.style('background-color')

      var affectedEdges = selectedNodes.forEach(function(node) {
        // Select edges with the same background color
        var matchingEdges = self.cy.edges('[source="' + node.id() + '"][target]') // Outgoing edges
                            .filter('[line-color="' + color + '"]');
        return matchingEdges
      });
      affectedEdges.style('line-color', color)
      this.cy.style().selector("edge").style("visibility", "visible").update()
    },

    rgb_to_hex(rgbString) {
      // Use regular expression to extract RGB components
      var match = rgbString.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);

      if (!match) {
        throw new Error('Invalid RGB string format');
      }

      // Extract individual RGB components
      var r = parseInt(match[1], 10);
      var g = parseInt(match[2], 10);
      var b = parseInt(match[3], 10);

      // Convert each component to a hex value
      var rHex = this.componentToHex(r);
      var gHex = this.componentToHex(g);
      var bHex = this.componentToHex(b);

      // Concatenate the hex values
      var hexColor = "#" + rHex + gHex + bHex;

      return hexColor;
    },

    componentToHex(c) {
      var hex = c.toString(16);
      return hex.length === 1 ? "0" + hex : hex;
    },

    contrast(hex) {
      var threshold = 130;
      let r = 0, g = 0, b = 0;

      // 3 digits
      if (hex.length == 4) {
        r = "0x" + hex[1] + hex[1];
        g = "0x" + hex[2] + hex[2];
        b = "0x" + hex[3] + hex[3];
      // 6 digits
      } else if (hex.length == 7) {
        r = "0x" + hex[1] + hex[2];
        g = "0x" + hex[3] + hex[4];
        b = "0x" + hex[5] + hex[6];
      }
      return ((r*0.299 + g*0.587 + b*0.114) > threshold) ? '#000000' : '#ffffff';
    }
  },
  computed: {
    isCommunityDetection(){
      return this.community_detection_methods.includes(this.experiment.category)
    }
  }

};
</script>

<style scoped>
.parent_container {
  text-align: left;
}

#container {
  min-height: 90vh;
  /* border-radius: 10px;
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px,
    rgba(60, 64, 67, 0.15) 0px 1px 3px 1px; */
}

</style>
// Copyright (c) nicolas allezard
// Distributed under the terms of the Modified BSD License.
//@ts-ignore
import {  DOMWidgetModel,  DOMWidgetView,  ISerializers,LayoutModel} from '@jupyter-widgets/base';

import '@material/mwc-dialog';


import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

//@ts-ignore
import {html,LitElement,customElement,css,property,directives} from 'lit-element';

 
import  "./playback-control"

//@ts-ignore
import {repeat} from 'lit-html/directives/repeat.js';


//@ts-ignore
const lock = html`<svg width="24" height="24" viewBox="0 0 24 24"><path d="M8 9v-3c0-2.206 1.794-4 4-4s4 1.794 4 4v3h2v-3c0-3.313-2.687-6-6-6s-6 2.687-6 6v3h2zm.746 2h2.831l-8.577 8.787v-2.9l5.746-5.887zm12.254 1.562v-1.562h-1.37l-12.69 13h2.894l11.166-11.438zm-6.844-1.562l-11.156 11.431v1.569h1.361l12.689-13h-2.894zm6.844 7.13v-2.927l-8.586 8.797h2.858l5.728-5.87zm-3.149 5.87h3.149v-3.226l-3.149 3.226zm-11.685-13h-3.166v3.244l3.166-3.244z"/></svg>`;
//@ts-ignore

const fastforward = html`<svg   version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M292.418,134.248c-8.331-8.331-21.839-8.331-30.17,0c-8.331,8.331-8.331,21.839,0,30.17L353.83,256l-91.582,91.582
		c-8.331,8.331-8.331,21.839,0,30.17c8.331,8.331,21.839,8.331,30.17,0l106.667-106.667c8.331-8.331,8.331-21.839,0-30.17
		L292.418,134.248z"/>
	  <path d="M271.085,240.915L164.418,134.248c-8.331-8.331-21.839-8.331-30.17,0s-8.331,21.839,0,30.17L225.83,256l-91.582,91.582
		c-8.331,8.331-8.331,21.839,0,30.17c8.331,8.331,21.839,8.331,30.17,0l106.667-106.667
		C279.416,262.754,279.416,249.246,271.085,240.915z"/>
</svg>`


//@ts-ignore
const left_arrow = html`<svg  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"

   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M309.416,152.144l-149.333,85.333c-14.332,8.19-14.332,28.855,0,37.045l149.333,85.333
		c14.222,8.127,31.918-2.142,31.918-18.523V170.667C341.333,154.286,323.638,144.017,309.416,152.144z M298.667,304.572
		L213.665,256l85.001-48.572V304.572z"/>
	  </svg>`

//@ts-ignore

const right_arrow = html`<svg  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">

	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M351.918,237.477l-149.333-85.333c-14.222-8.127-31.918,2.142-31.918,18.523v170.667
		c0,16.38,17.696,26.649,31.918,18.523l149.333-85.333C366.25,266.333,366.25,245.667,351.918,237.477z M213.333,304.572v-97.144
		L298.335,256L213.333,304.572z"/>
 </svg>`


//@ts-ignore

const rewind  = html`<svg  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	  viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">

	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M158.17,256l91.582-91.582c8.331-8.331,8.331-21.839,0-30.17c-8.331-8.331-21.839-8.331-30.17,0L112.915,240.915
		c-8.331,8.331-8.331,21.839,0,30.17l106.667,106.667c8.331,8.331,21.839,8.331,30.17,0c8.331-8.331,8.331-21.839,0-30.17
		L158.17,256z"/>
	  <path d="M377.752,134.248c-8.331-8.331-21.839-8.331-30.17,0L240.915,240.915c-8.331,8.331-8.331,21.839,0,30.17l106.667,106.667
		c8.331,8.331,21.839,8.331,30.17,0c8.331-8.331,8.331-21.839,0-30.17L286.17,256l91.582-91.582
		C386.083,156.087,386.083,142.58,377.752,134.248z"/>
 </svg>`

//@ts-ignore

const freeDrawing = html`<svg class="freeDrawing" version="1.1" x="0px" y="0px" viewBox="0 0 283.093 283.093" style="enable-background:new 0 0 283.093 283.093;" xml:space="preserve"><g><path d="M271.315,54.522L218.989,2.196c-2.93-2.928-7.678-2.928-10.607,0L78.274,132.303c-1.049,1.05-1.764,2.388-2.053,3.843l-12.964,65.29c-0.487,2.456,0.282,4.994,2.053,6.765c1.421,1.42,3.334,2.196,5.304,2.196c0.485,0,0.975-0.047,1.461-0.144l65.29-12.964c1.456-0.289,2.793-1.004,3.843-2.053L271.315,65.129C274.244,62.2,274.244,57.452,271.315,54.522z M83.182,178.114l6.776-34.127l39.566,39.566l-34.127,6.776L83.182,178.114z"/><path d="M205.912,227.066c-71.729-30.029-118.425,19.633-132.371,27.175c-17.827,9.641-42.941,20.97-48.779,1.358c-3.522-11.832,15.521-24.479,28.131-28.42c9.2-2.876,5.271-17.358-3.988-14.465c-19.582,6.121-42.948,22.616-38.851,45.839c3.044,17.256,24.67,32.995,66.368,11.114c30.308-15.902,50.897-48.84,114.733-31.783c20.969,5.602,37.92,19.27,45.178,40.057c3.168,9.07,17.662,5.169,14.465-3.988C243.062,251.799,227.411,236.067,205.912,227.066z"/></g></svg>`;

//box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
//@customElement('my-element' as any)
class litPolaroid extends LitElement {
   static properties = {
	caption: {type: String},
	image_data: {type: String},
	width:{type:Number},
	target:{type: String}

  };
  public jupyter_widget:any;
  public image_data:any
  public caption:string
  public width: number
  public height: number

  public carousel:any
  public target:string;
  static styles = [css`
	
	 div.polaroid {

	  display: flex;
	  flex-direction: column;

	  width: 200px;
	  
	  background-color: #FCFAEF; 
	  box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
	  
	  padding: 5px 2px 0px 2px;

	  align-items:center;
	  justify-content: space-around;
	  overflow: hidden;

	  margin-bottom:2px;
	  margin-top:5px;

	  margin-right:5px;

	  

	  border-radius: 8px;
	}
	div.polaroid[target=selected] {
	  transition: 0.2s;
	  background-color: #F2CCA7;
	  box-shadow: 4px 8px 8px 2px rgba(0, 0, 0, 0.2);
	   margin-top: 2px;
	   // margin-left: -2px;
	}
	 div.polaroid:hover{
	   transition: 0.2s;
	   box-shadow: 4px 8px 8px 2px rgba(0, 0, 0, 0.2);
	   // margin-top: -2px;
	   // margin-left: -2px;

	 }
	p.caption_class {
	  text-align: center;
	  width: 100%;
	  padding:0px;
	  margin:0px;
	  overflow-wrap: break-word;
	}
  `];
 

  constructor() {
	super();
	this.image_data='';
	this.caption=''
	this.width=200;
	this.height=220;
	this.jupyter_widget=null
	this.carousel=null
	this.target="unselected"
  }

  get caption_element(): HTMLDivElement {
	return this.shadowRoot!.querySelector("#image_caption") as HTMLDivElement;
  }


  _handleClick(e:any){
	//this.carousel.openZoom(this.image_data)
	if(e.ctrlKey){
		var modal = this.carousel.shadowRoot.getElementById("myModal");
		console.log(e)
		console.log(window.innerHeight)
		//console.log(this.carousel.jupyter_widget.getBoundingClientRect())
		var win_height=window.innerHeight
		var y_pos=win_height-850<e.y?win_height-850:e.y
		console.log("y_pos",y_pos)
		modal!.style.paddingTop=y_pos+"px"
		modal!.style.display = "block";
	 	const i=modal!.querySelector('.image_zoom') as HTMLImageElement;
	    i!.src=this.image_data
	}
	else{
		if (this.jupyter_widget){
			if (this.carousel.selected_id===this.id){
				this.target="unselected"
				this.carousel.selected_id=-1
				this.jupyter_widget.selected_id=[-1]
				this.jupyter_widget.model.set("selected_id",JSON.parse(JSON.stringify([-1]))); 
				this.jupyter_widget.touch();
			}
			else{
				this.carousel.selected_id=this.id
				this.jupyter_widget.selected_id=[this.id]
				this.jupyter_widget.model.set("selected_id",JSON.parse(JSON.stringify([this.id]))); 
				this.jupyter_widget.touch();
				this.carousel.deselect()
				this.target="selected"
				this.jupyter_widget.send({ event:{ selected: this.id }});
				this.jupyter_widget.touch()
			}
		}
	}
  }
  render() {
	const image_height=this.height
	//height:${this.height}px
	//${image_height}px
	return html`
	<div class="polaroid tooltip" style="width:${this.width}px;"  @click="${(e:any)=>this._handleClick(e)}"  target="${this.target}" >
	  <img class=myid src=${this.image_data} style=" width:100%;  height:${image_height}px; object-fit: contain; ">

	  <p class="caption_class" id="image_caption">
	  ${this.caption}
	  </p>
	</div>
	`;
  }
 
   
}
customElements.define('lit-polaroid', litPolaroid);
	//${this.image_list.map( (url:any) => html`<lit-polaroid  image_data=${url}></lit-polaroid>`) }


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



export class PolaroidModel extends DOMWidgetModel {
  defaults() {
	return {
	  ...super.defaults(),
	  _model_name: PolaroidModel.model_name,
	  _model_module: PolaroidModel.model_module,
	  _model_module_version: PolaroidModel.model_module_version,
	  _view_name: PolaroidModel.view_name,
	  _view_module: PolaroidModel.view_module,
	  _view_module_version: PolaroidModel.view_module_version,
	  _id: 'polaroid',
	  image:'',
	  im_format:'png',
	  width:200,
	  height:220,
	  selected:false

	};
  }
  initialize(attributes: any, options: any) {
	super.initialize(attributes, options);
	console.log("initialize")
	this.on('msg:custom', this.onMessage.bind(this));
	this.send({ event: 'client_ready' },{});//{ event: 'client_ready' }, {});
	
  }
  private async onMessage(message: any, buffers: any) {
	// Retrieve the commands buffer as an object (list of commands)
	console.log("command",message,buffers)
  }
  static serializers: ISerializers = {
	...DOMWidgetModel.serializers,
	// Add any extra serializers here
  };

  static model_name = 'PolaroidModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'PolaroidView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}



export class PolaroidView extends DOMWidgetView {
  polaroid:any
  // initialize(){
  //  this.el.style.setProperty("minWidth","400px")
  //   console.log(this.el.style)

  // }
  render() {
	this.el.classList.add("polaroid-widget")
	console.log("PolaroidView 6") 
   
	// const layout=this.model.get('layout')
	// layout.attributes["min_width"]="600px"
	// console.log("layout",layout);
  
	// this.setLayout(layout);
   
	console.log("size",this.model.get("width"),this.model.get("height"))

	this.polaroid=document.createElement("lit-polaroid");
	this.polaroid.width=this.model.get("width");
	this.polaroid.height=this.model.get("height");

	this.el.appendChild(this.polaroid)
	  
	var url='';
	const format = this.model.get('im_format');
	const value = this.model.get('image');
	console.log("format",format)
	if (format !== 'url') {
	  const blob = new Blob([value], {
		type: `image/${this.model.get('format')}`,
	  });
	  url = URL.createObjectURL(blob);
	} else {

	  url = value
	}
	console.log(url)
	this.polaroid.image_data=url;
	this.polaroid.caption=this.model.get('caption');
	this.model.on('change:image', this.image_changed, this);
	this.model.on('change:caption', this.caption_changed, this);
	this.model.on('change:selected', this.select_change, this);
	this.polaroid.addEventListener('mousedown', { handleEvent: this.onMouseDown.bind(this) });
	
	//this.polaroid.setAttribute('tabindex', '0');

  }
  

  private select_change(){
	const selected=this.model.get("selected")
	if (selected){
	  this.polaroid.shadowRoot.querySelector(".polaroid").setAttribute("target","selected")
	}
	else{
	  this.polaroid.shadowRoot.querySelector(".polaroid").setAttribute("target","unselected")
	}

  }

  private onMouseDown(event: MouseEvent) {
	// Bring focus to the canvas element, so keyboard events can be triggered
	this.polaroid.focus();
	console.log("onMouseDown",event.type)
	const msg={_id: '', type:'', buttons:-1};
	msg.type=event.type
	msg.buttons=event.buttons
	msg._id=this.model.get('_id');
	//this.polaroid.shadowRoot.querySelector(".polaroid").setAttribute("target","selected")
	this.send({ event: event.type, ...msg },);
   //this.send({ event_type :'toto event' });
  } 

  caption_changed(){
	const caption_element=this.polaroid.caption_element
   
	// console.log("cap .caption_class ",this.polaroid.shadowRoot.querySelector(".caption_class"))
	// console.log("cap #image_caption",this.polaroid.shadowRoot.querySelector("#image_caption"))
	caption_element.textContent=this.model.get('caption');
	this.polaroid.caption=this.model.get('caption');
	console.log("set caption",this.polaroid.caption)

  }
  image_changed() {
	var url='';
	console.log("image_changed")
	const format = this.model.get('im_format');
	const value = this.model.get('image');
	 console.log("format",format)
	if (format !== 'url') {
	  const blob = new Blob([value], {
		type: `image/${this.model.get('format')}`,
	  });
	  url = URL.createObjectURL(blob);
	} else {
	  url = value
	}
	console.log(url)
	this.polaroid.image_data=url;
	this.polaroid.caption=this.model.get('caption');

	this.polaroid.update()
  }
}







/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////








class litCarousel extends LitElement {
 
 static properties = {
   page_number:{type:Number}
 }


  static styles = [css`
	  .lit-carousel{
		display: flex;
		flex-direction: row;
		overflow: hidden;
		flex-wrap: wrap;
	  }
	.icon {
		 width:  30px;
		 height:  30px;

		  margin-bottom: 10px;
		  margin-left: 10px;
		  margin-right: 10px;
		  margin-top: 10px;
		  z-index: 1;
		  color: black;
		  background: white;
		  fill: #79005D;
		  padding: 10px;
		  border-radius: 50%;
		  cursor: pointer;
		   box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
		}

		.icon:hover {
		background:  #79005D;
		fill: white;
		 box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
	  }
	  .navigation{
		display: flex;
		width: 100%;
		align-items: center;
		align-content: center;
		justify-content: center;

	  }

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 99; /* Sit on top */
  padding-top: 400px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: fit-content;
  height: fit-content;

}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
	  `]

  //public image_list: {caption:String,url:String}[]
  public images_data:any
  public width: number
  public height: number

  public item_width :number
  public item_height :number

  public nb_per_page: number
  public page_number: number
  
  public nb_samples: number
  public nb_pages: number

  public polaroid_items:any
  public jupyter_widget:any
  public wrap_mode:string
  public selected_id:string;
  public wait:boolean
  public zoomMode:boolean

  count:number


  constructor(){
	super();
	//this.image_list=new Array()
	
	this.polaroid_items=new Array()
	this.width=800;
	this.height=400;

	this.item_width=200;
	this.item_height=200;

	this.nb_per_page=0;
	this.page_number=0;


	this.nb_samples=0;
	this.nb_pages=0;


	this.selected_id='none';

	this.wrap_mode="wrap";

	this.wait=false
	this.count=0
	this.zoomMode=false
  }


  deselect(){
	for (var i = 0; i < this.polaroid_items.length; ++i) {
	  if (this.polaroid_items[i]) this.polaroid_items[i].target="unselected"
	}
  }

  createItems(image_list?:any){

	// if (image_list){
	//   this.image_list=image_list
	// }

	console.log("createItems !!")
	
	this.nb_per_page= Math.floor(this.width/(this.item_width+9))*Math.floor(this.height/(this.item_height+10+20))


	this.polaroid_items=new Array(this.nb_per_page);

	for (var i = 0; i < this.polaroid_items.length; ++i) {
		  this.polaroid_items[i]= new litPolaroid()
		  if (this.images_data.has(i)){
			  this.polaroid_items[i].image_data=this.images_data.get(i).url
			  this.polaroid_items[i].caption=this.images_data.get(i).caption
		  }

		  //console.log(i,this.images_data.get(i).caption)

		  this.polaroid_items[i].jupyter_widget=this.jupyter_widget  
		  this.polaroid_items[i].id=i
		  this.polaroid_items[i].width=this.item_width
		  this.polaroid_items[i].height=this.item_height

		  this.polaroid_items[i].carousel=this
		  this.polaroid_items[i].style.order=i
	  
	  
	}

  }


  computeNbPages(){
	 this.nb_per_page= Math.floor(this.width/(this.item_width+9))*Math.floor(this.height/(this.item_height+10+20))
	 this.nb_pages=Math.floor(this.jupyter_widget.images_index.length/this.nb_per_page)+1
  }


  updatePageContent(begin:number,end:number){

		console.log("update index_page",this.page_number, "begin",begin,"end",end)

		var i_item=0
		for (var i = begin; i < end ; ++i,++i_item) {
			if (this.images_data.has(i)){

			  if (!this.polaroid_items[i_item])  this.polaroid_items[i_item]= new litPolaroid()
			  
			  //console.log(i,this.images_data.get(i).caption)
			 
			  this.polaroid_items[i_item].image_data=this.images_data.get(i).url
			  this.polaroid_items[i_item].id=i
			  this.polaroid_items[i_item].width=this.item_width
			  this.polaroid_items[i_item].height=this.item_height
			  this.polaroid_items[i_item].caption=this.images_data.get(i).caption
			  this.polaroid_items[i_item].carousel=this
			  this.polaroid_items[i_item].jupyter_widget=this.jupyter_widget

			  this.polaroid_items[i_item].style.order=i_item
			}
		//     //nbdone+=1
	  
		}
		//console.log("nb correct",i_item)
		for (var i = i_item; i <  this.polaroid_items.length; i++)   delete this.polaroid_items[i]


		this.deselect()
	  
		const match:any[]=this.polaroid_items.filter((item:any) => item.id===this.selected_id)

		if (match.length>0){
		  console.log(match)
		  match[0].target="selected"
		}

  }


  gotoPage(page_index:number){
	  if (this.wait) return

	  console.log("gotopage ",page_index)


	  this.nb_per_page= Math.floor(this.width/(this.item_width+9))*Math.floor(this.height/(this.item_height+10+20))
	  
	  this.nb_per_page = this.nb_per_page < this.polaroid_items.length ? this.nb_per_page : this.polaroid_items.length
	 
	  console.log("width",this.width,"height",this.height)


	  console.log("nb row ",Math.floor(this.width/(this.item_width+9)) )
	  console.log("nb col",Math.floor(this.height/(this.item_height+10+20)) )

	  console.log("this.nb_per_page",this.nb_per_page)

	  var begin = page_index*this.nb_per_page

	  begin = begin >0 ? begin : 0;
	  var end  = begin+this.nb_per_page

	  if (begin>=this.jupyter_widget.images_index.length) return

	  end = end<this.jupyter_widget.images_index.length ? end  : this.jupyter_widget.images_index.length;

	  begin = begin<this.jupyter_widget.images_index.length ? begin  : this.jupyter_widget.images_index.length;

	  //if (begin>=end) return

	  console.log("begin",begin,'end',end )
	  
	 //|| !((end-1) in this.jupyter_widget.data_indices)
	  // const missing=[]
	  // for (var i = begin; i < end; i++) {
		 // if ( !(this.jupyter_widget.images_data.has(i))){

			// missing.push(i)
		 //  }
	  // }
	  //console.log("missing",missing)
	  if ( !(this.jupyter_widget.images_data.has(begin)) || !(this.jupyter_widget.images_data.has(end-1)) ){
		
		this.count+=1
		this.wait=true 
		this.jupyter_widget.send({ send_data: [begin, end, this.count]});

		console.log("SEND ME DATA ",begin,end,this.count)

		//console.log("image_data",this.jupyter_widget.images_data.size)
	   
		this.jupyter_widget.data_received=false

		const waitFor = async (condFunc: () => boolean) => {
		  return new Promise<void>((resolve) => {
			if (condFunc()) {
			  resolve();
			} else {
			  console.log(".")
			  setTimeout(async () => {
									  await waitFor(condFunc);
									  resolve();
									  }, 
						400);
			}
		  });
		};

		const myFunc = async () => {
			
			await waitFor(() => (this.jupyter_widget.data_received=== true));

			console.log('!!!!!!! FINI D ATTENDRE');
			this.wait=false
			// this.page_number-=1
			
			this.updatePageContent(begin,end)


			this.update(this.jupyter_widget.image_list)
			
		};

		myFunc();
		return;

	  }

	  this.updatePageContent(begin,end)
	 this.wait=false 
	}

  updateItem(i:number){

	const match:any[]=this.polaroid_items.filter((item:any) => item.id===i.toString())
	
	if (match.length>0){
		  match[0].jupyter_widget=this.jupyter_widget  
		  //if (match[0].image_data)  URL.revokeObjectURL(match[0].image_data);
		  match[0].image_data=this.images_data.get(i).url
		  match[0].id=i
		  match[0].width=this.item_width
		  match[0].caption=this.images_data.get(i).caption
		  match[0].carousel=this
		  match[0].style.order=i
	}else{
	  console.log("NO MATCH WITH ",i)
	}


  }
	
   wheel_func(event:any){
	  event.preventDefault();
	  const delta = Math.sign(event.deltaY);
	  this.move_by(delta)
   }
   
  isNumeric(a:any) {
  if (typeof a != "string") return false // we only process strings!  
	return !isNaN(a as unknown as number) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
		   !isNaN(parseFloat(a)) // ...and ensure strings of whitespace fail
  }

  //style="z-index=9999; height=100%
	 get imageZoom() {
        return html`
        
        <mwc-dialog hideActions style="--mdc-dialog-z-index:99999999;--mdc-shape-medium: 0px; --mdc-dialog-max-width:800px; --mdc-dialog-padding-top: 400px;">
            
            <img class="image_zoom" style="height:400px; object-fit:contain; ">
           
            
           
        </mwc-dialog>
        `
    }
  
    openZoom(image:any) {
        const d = this.shadowRoot!.querySelector('mwc-dialog');
        d!.open = true;
        console.log(d!.style.marginTop)
        const i=d!.querySelector('.image_zoom') as HTMLImageElement;
        i!.src=image
    }

    // When the user clicks on <span> (x), close the modal
	closeModal() {
	  this.shadowRoot!.getElementById("myModal")!.style.display = "none";
	}

	onKeyDown(evt: KeyboardEvent) {
		console.log("key")
		if (evt.ctrlKey) {
			// ctrl down = remove
			this.zoomMode=true
		}
	}
	onKeyUp(evt: KeyboardEvent) {
				console.log("keyup")

		if (evt.ctrlKey) {
			// ctrl down = remove
			this.zoomMode=false
		}
	}
	protected keyHandlerBindDown: (evt: any) => void = this.onKeyDown.bind(this);
	protected keyHandlerBindUp: (evt: any) => void = this.onKeyUp.bind(this);

	firstUpdated(){
		// const root=this.shadowRoot!.getElementById("polaroidCarousel")
		// root!.addEventListener('keydown', this.keyHandlerBindDown);
		// root!.addEventListener('keyup', this.keyHandlerBindUp);

	 //modal!.style.display = "none";

	  // if (event.target == 'lit-element') {
	  //   modal!.style.display = "none";
	  // }
	}

	protected createRenderRoot() {
	    const root = super.createRenderRoot();
	    root.addEventListener('click',
	      	(e: Event) => {
		      	console.log((e.target as Element).id)

		      	var id_=(e.target as Element).id
		      	if (id_=='myModal'){
					this.closeModal()

		      	}
	  		}
	    );
	    return root;
  	}
	
  	render() {
		console.log("render carousel")
		return html`
			<div id="myModal" class="modal">
					<div class="modal-content">
					<span class="close" @click=${() => this.closeModal() } style="padding: 10px;">  &times </span>
						<img class="image_zoom" style="height:800px; object-fit:contain; ">
			  	</div>
			</div>

			<div class="lit-carousel" id="polaroidCarousel" tabIndex="1"
				 style="width:${this.width}px;; height:fit-content; flex-wrap:${this.wrap_mode}" 
				 @wheel=${(event:any) => this.wheel_func(event) }
			>
			  ${this.polaroid_items.map((item:any) => 
				html`${item}
				`)}
			  
			</div>
			<div class="navigation"  style="width:${this.width}px; " >
				<p>Page : ${this.page_number}/${this.nb_pages-1}</p>
				<p class="icon" title="Rewind"         @click=${() => this.move_by(-10) } >${rewind}</p>
			  	<p class="icon" title="Back"           @click=${() => this.move_by(-1) } >${left_arrow}</p>
			  	<p class="icon" title="Next"           @click=${() => this.move_by(1) } >${right_arrow}</p>
			  	<p class="icon" title="Fast Forward"   @click=${() => this.move_by(10) } >${fastforward}</p>
			</div>
			`
  	}

  move_by(step:number){
	if (this.wait) return
	var page_number=this.page_number+step
	
	this.computeNbPages()


	page_number=page_number>0?page_number:0;
	page_number=page_number<this.nb_pages?page_number:this.nb_pages-1;
	
	this.gotoPage(page_number)

	this.page_number=page_number;

  }
}
customElements.define('lit-carousel', litCarousel);




//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




export class CarouselModel extends DOMWidgetModel {
  defaults() {
	return {
	  ...super.defaults(),
	  _model_name: CarouselModel.model_name,
	  _model_module: CarouselModel.model_module,
	  _model_module_version: CarouselModel.model_module_version,
	  _view_name: CarouselModel.view_name,
	  _view_module: CarouselModel.view_module,
	  _view_module_version: CarouselModel.view_module_version,
	  _id: 'Carousel',
	  image_list:[],
	  image_index:[],
	  im_format:'png',
	  image_captions:[],
	  width:800,
	  item_with:200,
	  item_height:200,
	  selected_id:[]

	};



  }
   initialize(attributes: any, options: any) {
	super.initialize(attributes, options);
	console.log("initialize")
	//this.on('msg:custom', this.onMessage.bind(this));
	
	
  }

 

  static serializers: ISerializers = {
	...DOMWidgetModel.serializers,
	// Add any extra serializers here
  };

  static model_name = 'CarouselModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CarouselView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}


export class CarouselView extends DOMWidgetView {
	carousel:any 

	data_received:boolean

	images_data:any
	images_index:number[]
	selected_id:number[]


 	private async onMessage(message: any, buffers: any) {
		// Retrieve the commands buffer as an object (list of commands)
		console.log("command",message,"buffer",buffers)
		if ("set_image" in message){
			console.log("set_image",message.set_image.index,message.set_image.caption)
			var index=message.set_image.index,caption=message.set_image.caption,format=message.set_image.format
			var url=''
			if (this.images_data.has(index) ){
				console.log("found",index)
					if (buffers.length>0){
						console.log("with image")
						if (format !== 'url') {
							const blob = new Blob(buffers, { type: `image/${format}`,});
							url = URL.createObjectURL(blob);
						} else {
							url = (new TextDecoder('utf-8')).decode(buffers[0]);
						}

					//console.log(cap_list[i])    
					if (!caption) caption=this.images_data.get(index).caption

					this.images_data.set(index,{caption:caption, url:url,noerase:1} )
					console.log(this.images_data.get(index))
					this.carousel.updateItem(index)
				}
				else{
					console.log("no image")
					const old=this.images_data.get(index)
					this.images_data.set(index,{caption:caption, url:old.url,noerase:1} )
					this.carousel.updateItem(index)

				}
			}

		}

		console.log(this.images_data)

	  }
	render() {

		this.el.classList.add("Carousel-widget")

		console.log("CarouselView 7") 

		// const layout=this.model.get('layout')
		// layout.attributes["min_width"]="600px"
		// console.log("layout",layout);
		// this.setLayout(layout);


		this.images_index=this.model.get("images_index");
		console.log("this.images_index",this.images_index.length)

		const width=this.model.get("width");

		const height=this.model.get("height");

		const item_width=this.model.get("item_width")  
		const item_height=this.model.get("item_height")  
		 
		this.model.on('change:image_list', this.dataFromPython, this);
		this.model.on('change:selected_id', this.onSelectedId, this);
		this.model.on('msg:custom', this.onMessage.bind(this));

		this.carousel=document.createElement('lit-carousel') as litCarousel


		this.carousel.item_width=item_width;
		this.carousel.item_height=item_height;
		this.carousel.width=width;
		this.carousel.height=height;
		this.carousel.jupyter_widget=this

		
		this.images_data=new Map()

		this.updateImagesData()

		this.carousel.images_data=this.images_data
		this.carousel.computeNbPages()
		this.carousel.createItems()
		this.carousel.gotoPage(0)
		

		// POUR EFFACER IMAGE LIST 
		// this.model.set("image_list",JSON.parse(JSON.stringify(['-'])));
		// this.touch()


		this.data_received=false
	
		//console.log("step",step,(width/(item_width+14)))
		
		this.el.appendChild( this.carousel)
	  
		// const  playbackcontrol=document.createElement("playback-control") as any
		// playbackcontrol.max=100;
		// playbackcontrol.current=0;

		// this.el.appendChild(playbackcontrol)

  	}
 


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	onSelectedId(){
		console.log("selected_id",this.selected_id)
		
	}



	dataFromPython(){

		this.data_received=false

		console.log("dataFromPython",)

		if (this.updateImagesData()){
			this.carousel.images_data=this.images_data
			this.data_received=true
		}
		this.data_received=true
	}


  	updateImagesData(){
	  
		const im_list = this.model.get('image_list');
		
		if (im_list[0]==='-'){
			console.log("liste vide")
			return false
		}
		//console.log(im_list[0][0])

	  	console.log("updateImagesData",im_list.length)
	  
		var url='';
		const nb_to_come=im_list.length

		if (nb_to_come+this.images_data.size>100){
			console.log("CLEANING")
			const nb_to_remove=nb_to_come+this.images_data.size-100
			var i=0
			var nb_remove=0
			while (nb_remove<nb_to_remove){
				if(this.images_data.has(i)){
					//console.log("remove",i)
					if (!("noerase" in this.images_data.get(i))) {
						URL.revokeObjectURL(this.images_data.get(i).url);
						this.images_data.delete(i)
						nb_remove++
					}
				}
				i++
				if (i>this.images_data.size) break
			}
			console.log(".................... REMOVED ",nb_remove)
		}

	
		const cap_list = this.model.get('image_captions');

		const cap_list_tmp= new Array(im_list.length)  

		for (var i = 0; i < im_list.length; i++) {

			const image_index=im_list[i][1]

			if (!this.images_data.has(image_index)) {
				//console.log("add new image_index",image_index)

				if (this.model.get('format') !== 'url') {
					const blob = new Blob([im_list[i][0]], { type: `image/${this.model.get('format')}`,});
					url = URL.createObjectURL(blob);
				} else {
					url = im_list[i][0]
				}

				//console.log(cap_list[i])    
				if (cap_list[ image_index ]){
					cap_list_tmp[i]=cap_list[image_index]
				}
				else{
					cap_list_tmp[i]=image_index
				}

				this.images_data.set(image_index,{caption:cap_list_tmp[i], url:url} )

			}


		}

		console.log("NEW IMAGES DATA size",this.images_data.size)
		this.model.set("image_list",JSON.parse(JSON.stringify(['-'])));
		this.touch()

		return true
	}

}























// var interval:number; //set scope here so both functions can access it
	
//     fastforward_.firstElementChild!.addEventListener("mousedown", function() {
//       avance_func(step*10);
//       interval = setInterval(()=>avance_func(step*10), 300); //500 ms - customize for your needs
//     });
	
//     fastforward_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) clearInterval(interval );
	  
//     })

//     right_.firstElementChild!.addEventListener("mousedown", function() {
//       avance_func(step);
//       interval = setInterval(()=>avance_func(step), 300); //500 ms - customize for your needs
//     });
	
//     right_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) clearInterval(interval );
	  
//     })

//     left_.firstElementChild!.addEventListener("mousedown", function() {
//       recule_func(step);
//       interval = setInterval(()=>recule_func(step), 300); //500 ms - customize for your needs
//     });
//     left_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) { clearInterval(interval ); }
//     });

//     rewind_.firstElementChild!.addEventListener("mousedown", function() {
//       recule_func(step*10);
//       interval = setInterval(()=>recule_func(step*10), 300); //500 ms - customize for your needs
//     });
	
//     rewind_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) clearInterval(interval );
	  
//     })



//     function avance_func(step:number) {
//       that.pos+=1

//       that.carousel.gotoPage(that.pos)
//       console.log(that.pos)
//       // if (that.pos>that.image_and_captions.length-2)  that.pos=that.image_and_captions.length-2
		
//       // const w=item_width+14//that.carousel.shadowRoot.querySelector("#carousel_item_1").getBoundingClientRect()["width"]
//       // console.log(that.pos,w*that.pos)
//       // that.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:w*that.pos-2,behavior:'smooth'}) 
	  
//     }
//     function recule_func(step:number) {
//       that.pos-=1

//       if (that.pos<0) that.pos=0

//         that.carousel.gotoPage(that.pos)
//       console.log(that.pos)
//       //   const w=item_width+14
//       //   console.log(that.pos,w*that.pos)
	  
//       // console.log(that.carousel.shadowRoot.querySelector("#carousel_item_1").getBoundingClientRect())
	  
//       //that.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:w*that.pos-2,behavior:'smooth'}) 

//     } 

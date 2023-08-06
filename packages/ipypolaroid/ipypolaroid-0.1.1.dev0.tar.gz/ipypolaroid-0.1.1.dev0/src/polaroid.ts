import {  DOMWidgetModel,  DOMWidgetView,  ISerializers} from '@jupyter-widgets/base';

import '@material/mwc-dialog';


import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

//@ts-ignore
import {html,LitElement,customElement,css,property,directives} from 'lit-element';

import { polaroid_styles} from "./style"


export class litPolaroid extends LitElement {
   
	static get styles() {
    	return polaroid_styles;
  	} 
  
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

  	public zoomHeight:number
 

	constructor() {
		super();
		this.image_data='';
		this.caption=''
		this.width=200;
		this.height=220;
		this.jupyter_widget=null
		this.carousel=null
		this.target="unselected"
		this.zoomHeight=600
	}

	get caption_element(): HTMLDivElement {
		return this.shadowRoot!.querySelector("#image_caption") as HTMLDivElement;
	}
  	_handleDoubleClick(e:any){
		
		var modal = this.shadowRoot!.getElementById("myModal");
		// console.log(e)
		// console.log(window.innerHeight)
		//console.log(this.carousel.jupyter_widget.getBoundingClientRect())
		var win_height=window.innerHeight
		var y_pos=win_height-(this.zoomHeight+50)<e.y?win_height-(this.zoomHeight+50):e.y
		// console.log("y_pos",y_pos)
		modal!.style.paddingTop=y_pos+"px"
		modal!.style.display = "block";
	 	const img=modal!.querySelector('.image_zoom') as HTMLImageElement;
	    img!.src=this.image_data
	
		
	}
  	_handleClick(e:any){

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
	closeModal() {
	  this.shadowRoot!.getElementById("myModal")!.style.display = "none";
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
		const image_height=this.height
		//height:${this.height}px
		//${image_height}px
		return html`
		<div class="polaroid tooltip" style="width:${this.width}px;"  @click="${(e:any)=>this._handleClick(e)}"  @dblclick="${(e:any)=>this._handleDoubleClick(e)}" target="${this.target}" >
		
			<img class=myid src=${this.image_data} style=" width:100%;  height:${image_height}px; object-fit: contain; ">

			<p class="caption_class" id="image_caption">
				${this.caption}
			</p>
		</div>
		<div id="myModal" class="modal">
			<div class="modal-content">
				<span class="close"      style="padding: 10px;"  @click=${() => this.closeModal()} > &times </span>
				<img  class="image_zoom" style="height:${this.zoomHeight}px; object-fit:contain; " >
	  			</div>
			
		</div>
		`;
	}

   
}
customElements.define('lit-polaroid', litPolaroid);


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
  
  render() {
	this.el.classList.add("polaroid-widget")
	console.log("PolaroidView 6") 
   
	// const layout=this.model.get('layout')
	// layout.attributes["min_width"]="600px"
	// console.log("layout",layout);
  
	// this.setLayout(layout);
   
	//console.log("size",this.model.get("width"),this.model.get("height"))

	this.polaroid=document.createElement("lit-polaroid");
	this.polaroid.width=this.model.get("width");
	this.polaroid.height=this.model.get("height");

	this.el.appendChild(this.polaroid)
	  
	var url='';
	const format = this.model.get('im_format');
	const value = this.model.get('image');
	//console.log("format",format)
	if (format !== 'url') {
	  const blob = new Blob([value], {
		type: `image/${this.model.get('format')}`,
	  });
	  url = URL.createObjectURL(blob);
	} else {

	  url = value
	}
	//console.log(url)
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




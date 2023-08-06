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
//@ts-ignore
import {repeat} from 'lit-html/directives/repeat.js';
//@ts-ignore
import  "./playback-control"

import  {fastforward,rewind,left_arrow,right_arrow,carousel_styles} from "./style"

import {litPolaroid} from "./polaroid"


class litCarousel extends LitElement {
 
	static properties = {
		page_number:{type:Number}
	}


  	static get styles() {
    	return carousel_styles;
  	} 
  

	//public image_list: {caption:String,url:String}[]
	public images_data:any
	public width: string
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

  	private count:number


  	constructor(){
		super();
		//this.image_list=new Array()
		
		this.polaroid_items=new Array()
		this.width="100%";
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
  	}


	deselect(){
		for (var i = 0; i < this.polaroid_items.length; ++i) {
		  if (this.polaroid_items[i]) this.polaroid_items[i].target="unselected"
		}
	}


  	createItems(image_list?:any){
		console.log("createItems !!")
		
		//this.nb_per_page= Math.floor(this.width/(this.item_width+9))*Math.floor(this.height/(this.item_height+10+20))


		this.polaroid_items=new Array(this.nb_per_page);

		for (var i = 0; i < this.polaroid_items.length; ++i) {
			this.polaroid_items[i]= new litPolaroid()
			if (this.images_data.has(i)){
				this.polaroid_items[i].image_data=this.images_data.get(i).url
				this.polaroid_items[i].caption=this.images_data.get(i).caption
			}

			if (this.jupyter_widget) 
				this.polaroid_items[i].jupyter_widget=this.jupyter_widget  

			this.polaroid_items[i].id=i
			this.polaroid_items[i].width=this.item_width
			this.polaroid_items[i].height=this.item_height
			this.polaroid_items[i].carousel=this
			this.polaroid_items[i].style.order=i
		}

  	}


	computeNbPages(){
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

		if (match.length>0) 	match[0].target="selected"
		

  }


  gotoPage(page_index:number){
	  if (this.wait) return

	  console.log("gotopage ",page_index)

	  console.log("carousel width",this.width)

	  console.log("this.nb_per_page",this.nb_per_page)

	  var begin = page_index*this.nb_per_page

	  begin = begin >0 ? begin : 0;
	  var end  = begin+this.nb_per_page

	  if (begin>=this.jupyter_widget.images_index.length) return

	  end = end<this.jupyter_widget.images_index.length ? end  : this.jupyter_widget.images_index.length;

	  // begin = begin<this.jupyter_widget.images_index.length ? begin  : this.jupyter_widget.images_index.length;

	  // if (begin>=end) return

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
	
  
	isNumeric(a:string) {
		return !isNaN(parseFloat(a)) //!isNaN(a ) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
	}

	get imageZoom() {
        return html`
        <mwc-dialog hideActions style="--mdc-dialog-z-index:99999999; --mdc-dialog-max-width:800px; ">
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

  
	onKeyDown(evt: KeyboardEvent) {
		console.log("key")
		if (evt.ctrlKey) {
			// ctrl down = remove
			//this.zoomMode=true
		}
	}

	onKeyUp(evt: KeyboardEvent) {
		console.log("keyup")

		if (evt.ctrlKey) {
			// ctrl down = remove
			//this.zoomMode=false
		}
	}
	protected keyHandlerBindDown: (evt: any) => void = this.onKeyDown.bind(this);
	protected keyHandlerBindUp: (evt: any) => void = this.onKeyUp.bind(this);

	
  	render() {
		console.log("render carousel")
		
		var width=this.width
		if (this.isNumeric(width)) 	width=width+"px"

		console.log("render with",width)
		return html`

			<div class="lit-carousel" id="polaroidCarousel" 
				 style="width:${width}; height:fit-content; flex-wrap:${this.wrap_mode} padding:5px" 
				 @wheel=${(event:any) => this.wheel_func(event) }
			>
			  ${this.polaroid_items.map((item:any) => html`${item}` )}
			  
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


 	wheel_func(event:any){
		event.preventDefault();
		var delta = Math.sign(event.deltaY);
		if (event.ctrlKey) delta=delta*10
		this.move_by(delta)
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
	  width:"100%",
	  item_with:200,
	  item_height:200,
	  selected_id:[],
	  n:10
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


 	
	render() {

		this.el.classList.add("Carousel-widget")

		console.log("CarouselView 9") 

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
		console.log("jupyter_widget width",width,height)
 
		this.model.on('change:image_list', this.dataFromPython, this);
		this.model.on('change:selected_id', this.onSelectedId, this);
		this.model.on('msg:custom', this.onMessage.bind(this));

		this.carousel=document.createElement('lit-carousel') as litCarousel


		this.carousel.item_width=item_width;
		this.carousel.item_height=item_height;
		this.carousel.width=width;
		this.carousel.height=height;
		console.log("this.model.get n",this.model.get("n"))
		this.carousel.nb_per_page=this.model.get("n");;

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


	private async onMessage(message: any, buffers: any) {

		console.log("command",message,"buffer",buffers)
		
		if ("set_image" in message){
			console.log("set_image",message.set_image.index,message.set_image.caption)
			var index=message.set_image.index,caption=message.set_image.caption,format=message.set_image.format
			var url=''

			if (this.images_data.has(index) ){

				console.log("image to change found",index)

				if (buffers.length>0){
					console.log("with image")
					if (format !== 'url') {
						const blob = new Blob(buffers, { type: `image/${format}`,});
						url = URL.createObjectURL(blob);
					} else {
						url = (new TextDecoder('utf-8')).decode(buffers[0]);
					}

					//console.log(cap_list[i])    
					if (!caption) 
						caption=this.images_data.get(index).caption

					this.images_data.set(index,{caption:caption, url:url,noerase:1} )
					//console.log(this.images_data.get(index))
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



	onSelectedId(){
		console.log("selected_id",this.selected_id)
		
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

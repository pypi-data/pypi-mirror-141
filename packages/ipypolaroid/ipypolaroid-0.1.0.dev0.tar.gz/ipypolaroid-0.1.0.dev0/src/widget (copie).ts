// Copyright (c) nicolas allezard
// Distributed under the terms of the Modified BSD License.
//@ts-ignore
import {  DOMWidgetModel,  DOMWidgetView,  ISerializers,LayoutModel} from '@jupyter-widgets/base';



import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

//@ts-ignore
import {html,LitElement,customElement,css,property,directives} from 'lit-element';



//@ts-ignore

import {repeat} from 'lit-html/directives/repeat.js';
//@ts-ignore
const lock = html`<svg width="24" height="24" viewBox="0 0 24 24"><path d="M8 9v-3c0-2.206 1.794-4 4-4s4 1.794 4 4v3h2v-3c0-3.313-2.687-6-6-6s-6 2.687-6 6v3h2zm.746 2h2.831l-8.577 8.787v-2.9l5.746-5.887zm12.254 1.562v-1.562h-1.37l-12.69 13h2.894l11.166-11.438zm-6.844-1.562l-11.156 11.431v1.569h1.361l12.689-13h-2.894zm6.844 7.13v-2.927l-8.586 8.797h2.858l5.728-5.87zm-3.149 5.87h3.149v-3.226l-3.149 3.226zm-11.685-13h-3.166v3.244l3.166-3.244z"/></svg>`;
//@ts-ignore

const fastforward = html`<svg class="fastforward"  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
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
const left_arrow = html`<svg class="fastforward" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"

   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
      <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
        c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
        z"/>
      <path d="M309.416,152.144l-149.333,85.333c-14.332,8.19-14.332,28.855,0,37.045l149.333,85.333
        c14.222,8.127,31.918-2.142,31.918-18.523V170.667C341.333,154.286,323.638,144.017,309.416,152.144z M298.667,304.572
        L213.665,256l85.001-48.572V304.572z"/>
      </svg>`

//@ts-ignore

const right_arrow = html`<svg class="fastforward" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">

      <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
        c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
        z"/>
      <path d="M351.918,237.477l-149.333-85.333c-14.222-8.127-31.918,2.142-31.918,18.523v170.667
        c0,16.38,17.696,26.649,31.918,18.523l149.333-85.333C366.25,266.333,366.25,245.667,351.918,237.477z M213.333,304.572v-97.144
        L298.335,256L213.333,304.572z"/>
 </svg>`


//@ts-ignore

const rewind  = html`<svg class="fastforward" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
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
    width:{type:Number}

  };
  public parent:any;
  public image_data:any
  public caption:string
  public width: number
  public height: number

  public carousel:any
  static styles = [css`
    
     div.polaroid {
      display: flex;
      flex-direction: column;
      width: 200px;
      
      background-color: #FCFAEF; 
      box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
      padding: 5px 2px 0px 2px;
      border: black 5px;
      align-items:center;
      justify-content: space-around;
      overflow: hidden;
      margin-bottom:10px;
      margin-top:5px;
      margin-right:10px;
      transition: 0.2s;
      border-radius: 5px;
    }
    div.polaroid[target=selected] {
      background-color: #F2CCA7;
      box-shadow: 4px 8px 8px 2px rgba(0, 0, 0, 0.2);
       margin-top: 2px;
       // margin-left: -2px;
    }
     div.polaroid:hover{
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
    this.parent=null
  }

  get caption_element(): HTMLDivElement {
    return this.shadowRoot!.querySelector("#image_caption") as HTMLDivElement;
  }
  _handleClick(e:any){
    console.log("_handleClick",this.id,this.parent)
    if (this.parent){
        //this.parent.model.send({ polaroid_id : this.caption });
        this.carousel.deselect()
        this.shadowRoot!.querySelector(".polaroid")!.setAttribute("target","selected")

        this.parent.model.set( "id_polaroid__selected" , JSON.parse(JSON.stringify(this.id)) );
        this.parent.send({ polaroid_id: this.id });
        this.parent.touch()
    }
  }
  render() {
    //const image_height=this.height-20
    //height:${this.height}px
    //${image_height}px
    return html`
    <div class="polaroid tooltip" style="width:${this.width}px; "  @click="${(e:any)=>this._handleClick(e)}" >
      <img class=myid src=${this.image_data} style="width:100%; object-fit: contain; height:"auto">

      <p class="caption_class" id="image_caption">
      ${this.caption}
      </p>
    </div>
    `;
  }
 
   
}
customElements.define('lit-polaroid', litPolaroid);
    //${this.image_list.map( (url:any) => html`<lit-polaroid  image_data=${url}></lit-polaroid>`) }





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
  protected getCoordinates(event: MouseEvent | Touch) {
    //const rect = this.el.getBoundingClientRect();

    const x = 0
    const y = 0

    return { x, y };
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

  static styles = [css`
      .lit-carousel{
        display: flex;
        flex-direction: row;
        overflow: hidden;
        flex-wrap: wrap;
      }`]

  public image_list: {caption:String,url:String}[]
  public width: number
  public item_width :number
  public items:any
  public parent:any
  public wrap_mode:string
  constructor(){
    super();
    this.image_list=new Array()
    this.width=800;
    this.item_width=200;
    this.wrap_mode="wrap";
  }
  deselect(){
    console.log("deselect")
    for (var i = 0; i < this.items.length; ++i) {
      this.items[i].shadowRoot.querySelector(".polaroid").setAttribute("target","unselected")
    }
  }
  render() {
    //console.log('litcarousel',this.image_list)
    //height:${this.height}px
    console.log("carousel parent",this.parent)
    
    this.items=new Array(this.image_list.length);

    for (var i = 0; i < this.items.length; ++i) {
      this.items[i]= new litPolaroid()

      // html`
      //  <lit-polaroid id="carousel_item_${i}" width=${this.item_width}  caption=${this.image_list[i].caption} image_data=${this.image_list[i].url}></lit-polaroid>
      // `
      this.items[i].parent=this.parent  
      this.items[i].image_data=this.image_list[i].url
      this.items[i].id="carousel_item"+i
      this.items[i].width=this.item_width
      this.items[i].caption=this.image_list[i].caption
      this.items[i].carousel=this
      this.items[i].style.order=1000-i
    }
    
    // return html`
    // <div class="lit-carousel" style="width:${this.width}px; " >
    //   ${repeat(this.image_list, (infos) => infos, (infos, index) => html`
    //    <lit-polaroid id="carousel_item_${index}" width=${this.item_width}  caption=${infos.caption} image_data=${infos.url}></lit-polaroid>
    //   `)}
    // </div>
    // `;
     return html`
    <div class="lit-carousel" style="width:${this.width}px; flex-wrap:${this.wrap_mode} " >
      ${this.items.map((item:any) => html`${item}`)}
    </div>
    `;
  }
}
customElements.define('lit-carousel', litCarousel);








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
      im_format:'png',
      image_captions:[],
      width:800,
      item_with:200,
      id_polaroid__selected:''

    };



  }
   initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    console.log("initialize")
    this.send({ event: 'carousel ready' },{});//{ event: 'client_ready' }, {});
    
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
  image_and_captions:any[]
  pos:number
  // initialize(){
  //  this.el.style.setProperty("minWidth","400px")
  //   console.log(this.el.style)
 
  // }
  render() {
    this.el.classList.add("Carousel-widget")
    console.log("CarouselView 7") 
       const that=this


    // const layout=this.model.get('layout')
    // layout.attributes["min_width"]="600px"
    // console.log("layout",layout);
    // this.setLayout(layout);
    const width=this.model.get("width");
    const item_width=this.model.get("item_width")  
     
    const step=Math.floor(width/(item_width+14))

    this.model.on('change:image_list', this.update_imgages_from_python, this);
    this.model.on('change:id_polaroid__selected', this.polaroid__selected, this);

    this.carousel=document.createElement('lit-carousel') as litCarousel
    this.carousel.item_width=item_width;
    this.carousel.width=width;
    this.carousel.parent=that

 
    this.update_image_and_captions()
    this.carousel.image_list=this.image_and_captions
    
    this.model.set("image_list",JSON.parse(JSON.stringify(['-'])));
    this.touch()
    console.log("liste",this.model.get("image_list"))






    const fastforward_=fastforward.getTemplateElement().content
    const left_=left_arrow.getTemplateElement().content
    const right_=right_arrow.getTemplateElement().content
    const rewind_=rewind.getTemplateElement().content
    console.log(left_)
   
    // const avance=document.createElement('button')
    // avance!.innerText='avance'
    
    this.pos=0
    console.log("step",step,(width/(item_width+14)))
    var interval:number; //set scope here so both functions can access it
    
    fastforward_.firstElementChild!.addEventListener("mousedown", function() {
      avance_func(step*10);
      interval = setInterval(()=>avance_func(step*10), 300); //500 ms - customize for your needs
    });
    
    fastforward_.firstElementChild!.addEventListener("mouseup", function() {
      if (interval ) clearInterval(interval );
      
    })

    right_.firstElementChild!.addEventListener("mousedown", function() {
      avance_func(step);
      interval = setInterval(()=>avance_func(step), 300); //500 ms - customize for your needs
    });
    
    right_.firstElementChild!.addEventListener("mouseup", function() {
      if (interval ) clearInterval(interval );
      
    })

    left_.firstElementChild!.addEventListener("mousedown", function() {
      recule_func(step);
      interval = setInterval(()=>recule_func(step), 300); //500 ms - customize for your needs
    });
    left_.firstElementChild!.addEventListener("mouseup", function() {
      if (interval ) { clearInterval(interval ); }
    });

    rewind_.firstElementChild!.addEventListener("mousedown", function() {
      recule_func(step*10);
      interval = setInterval(()=>recule_func(step*10), 300); //500 ms - customize for your needs
    });
    
    rewind_.firstElementChild!.addEventListener("mouseup", function() {
      if (interval ) clearInterval(interval );
      
    })


    this.el.addEventListener("wheel", event => {
      event.preventDefault();
        const delta = Math.sign(event.deltaY);
        console.info(delta);
        if (delta>0){
        avance_func(delta)
        }
        else{
          recule_func(-delta)
        }
    });

    function avance_func(step:number) {
      that.pos+=step
      console.log(that.pos)
      if (that.pos>that.image_and_captions.length-2)  that.pos=that.image_and_captions.length-2
        
      const w=item_width+14//that.carousel.shadowRoot.querySelector("#carousel_item_1").getBoundingClientRect()["width"]
      console.log(that.pos,w*that.pos)
      that.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:w*that.pos-2,behavior:'smooth'}) 
      
    }
    function recule_func(step:number) {
      that.pos-=step
      if (that.pos<0) that.pos=0
        const w=item_width+14
        console.log(that.pos,w*that.pos)
      //that.carousel.shadowRoot.querySelector("#carousel_item_1").getBoundingClientRect()["width"]
      that.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:w*that.pos-2,behavior:'smooth'}) 

    }

    this.el.appendChild( this.carousel)
    // this.el.appendChild(recule)
    // this.el.appendChild(avance)
    const navigation=document.createElement("div")
navigation.classList.add("navigation")
   navigation.appendChild(rewind_)
    navigation.appendChild(left_)
    navigation.appendChild(right_)
    navigation.appendChild(fastforward_)
    this.el.appendChild(navigation)
    // this.polaroid.setAttribute('tabindex', '0');
  }
 


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

polaroid__selected(){
  console.log("polaroid__selected",this.model.get("polaroid__selected"))
}

  update_imgages_from_python(){
    console.log("update_imgages_from_python",)
    if (this.update_image_and_captions()){
        this.carousel.image_list=this.image_and_captions
        this.pos=0
        this.carousel.update()
        this.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:0})
    }

  }
  update_image_and_captions(){
      console.log("update_image_and_captions")
      const im_list = this.model.get('image_list');
      

      if (im_list[0]==='-'){
        console.log("liste vide")
        return false
      }
      var url='';
      if (this.image_and_captions){
          for (var i = 0; i < this.image_and_captions.length; i++) {
              if (this.image_and_captions[i])  URL.revokeObjectURL(this.image_and_captions[i]);
          }
      }


      this.image_and_captions = new Array()  

    
      const cap_list = this.model.get('image_captions');
      const cap_list_tmp= new Array(im_list.length)  

      for (var i = 0; i < im_list.length; i++) {
          if (this.model.get('format') !== 'url') {
              const blob = new Blob([im_list[i]], { type: `image/${this.model.get('format')}`,});
              url = URL.createObjectURL(blob);
          } else {
              url = im_list[i]
          }
          //console.log(cap_list[i])    
          if (cap_list[i]){
              cap_list_tmp[i]=cap_list[i]
            
          }
          else{
              cap_list_tmp[i]=i
          }

          //console.log(i,im_list[i],cap_list[i])
          this.image_and_captions.push({caption:cap_list_tmp[i], url:url} )

      }
      //console.log("liste blob",this.image_and_captions)   
     return true
  }
     
}
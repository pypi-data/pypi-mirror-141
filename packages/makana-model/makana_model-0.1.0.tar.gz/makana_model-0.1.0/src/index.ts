import { IDisposable, DisposableDelegate } from '@lumino/disposable';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { Dialog, showDialog, ToolbarButton } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { DocumentRegistry } from '@jupyterlab/docregistry';

import {
  NotebookPanel,
  INotebookModel,
} from '@jupyterlab/notebook';

/**
 * The plugin registration information.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: 'makana-model',
  autoStart: true,
};
let accessToken: any=null;
var models: any;
let frameworkName:any;
let fileData: any;
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
   createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const trans = panel.translator.load('jupyterlab');
    const saveBtn = Dialog.okButton({ label: trans.__('Save') });
    var urlencoded = new URLSearchParams();
    urlencoded.append("client_id", "makana_api");
    urlencoded.append("grant_type", "client_credentials");
    urlencoded.append("scope", "makanaapp_api");
    urlencoded.append("client_secret", "TAxhx@9tH(l^MgQ9FWE8}T@NWUT9U)");
    fetch('https://makana-app-staging-wa.azurewebsites.net/connect/token',{
      method:'POST',
      headers:{
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: urlencoded,
      })
      .then((response) => response.json())
      .then((data)=>{
        fetch('https://makana-app-staging-wa.azurewebsites.net/api/makana/modelframeworks',{
        method:'GET',
        headers:{
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + data.access_token
        },
        }).then((response) => response.json())
        .then((data) => {
            models = data;
          })
        })
      .catch((error) => {
          console.error('Error:', error)
      });
    const modelRegister = () => {
      showDialog({
        title: "Register New Model",
        body: new SaveWidget(),
        buttons: [Dialog.cancelButton(), saveBtn]
        }).catch((e) => console.log(e));
    };

    const registerModel = new ToolbarButton({
      className: 'clear-output-button',
      label: 'Register New Model',
      onClick: modelRegister,
      tooltip: 'Register a New Model',
    });

    panel.toolbar.insertItem(10, 'registermodel', registerModel);

    return new DisposableDelegate(() => {
      registerModel.dispose();
    });
  }
}

class SaveWidget extends Widget {
  /**
   * Construct a new save widget.
   */
  constructor() {
    super({ node: createSaveNode() });
  }
  /**
   * Get the value for the widget.
   */
  getValue(): string {
    var frameName;
    var modelName = (document.getElementById('model') as HTMLInputElement).value;
    var description = (document.getElementById('desinput') as HTMLInputElement).value;
    var modelFramework = (document.getElementById('framework') as HTMLInputElement).value;
    var frameVer = (document.getElementById('framever') as HTMLInputElement).value;
    var modelForm = new FormData();
    modelForm.append('id',"");
    modelForm.append('name', modelName);
    modelForm.append('description', description);
    modelForm.append('modelFrameworkId', modelFramework);
    if(!frameworkName){
      frameName = (document.getElementById('framename') as HTMLInputElement).value;
      modelForm.append('frameworkName', frameName);
    }else{
      modelForm.append('frameworkName', frameworkName);
    }
    modelForm.append('frameworkVersion', frameVer);
    modelForm.append('modelFileName', fileData[0].name);
    modelForm.append('modelFileUri', "");
    modelForm.append('modelFile',fileData[0]);
    console.log(modelForm);
    fetch('https://localhost:44350/api/makana/models', {
      method: 'POST',
      headers:{
        'Authorization': 'Bearer ' + accessToken 
      },
      body: modelForm,
    }).then((response) => response.json())
    .then((data) => {
      console.log(data);
    }).catch((error) => {
      console.error('Error', error);
    });
    return (this.node as HTMLInputElement).value;
  }
}

function createSaveNode(): HTMLElement{
  var urlencoded = new URLSearchParams();
  urlencoded.append("client_id", "makana_api");
  urlencoded.append("grant_type", "client_credentials");
  urlencoded.append("scope", "makanaapp_api");
  urlencoded.append("client_secret", "TAxhx@9tH(l^MgQ9FWE8}T@NWUT9U)");
  fetch('https://localhost:44350/connect/token',{
    method: 'POST',
    headers: {
      'Content-Type' : 'application/x-www-form-urlencoded'
    },
    body: urlencoded
  }).then((response) => response.json())
  .then((data) => {
    accessToken = data.access_token;
  });
  const select = document.createElement('select');
  select.setAttribute("id", "framework");
  select.className = 'framework';
  const div = document.createElement('div');
  div.id = 'div';
  div.setAttribute('class', 'form-group row has-feedback-icon');
  div.style.lineHeight = '10px';
  const modelname = document.createElement('label');
  modelname.append('Model Name: ');
  const name = document.createElement('input');
  name.placeholder = 'Enter Model Name';
  name.id = 'model';
  const des = document.createElement('label');
  des.append('Description: ');
  const desinput = document.createElement('input');
  desinput.id = 'desinput';
  desinput.placeholder = 'Enter Description';
  const modelframe = document.createElement('label');
  modelframe.append('Model Framework: ');
  
  models.forEach(function(key: any){
    var option = document.createElement("option");
    option.value = key.id;
    option.text = key.name;
    select.appendChild(option);
  });
  
  const framename = document.createElement('label');
  framename.append('Framework Name: ');
  framename.setAttribute('class', 'd-none form-group row');
  const framenameinput = document.createElement('input');
  framenameinput.id = 'framename';
  framenameinput.setAttribute('class', 'd-none form-group row');
  framenameinput.placeholder = 'Enter Framework Name';
  const framever = document.createElement('label');
  framever.append('Framework Version: ');
  const frameverinput = document.createElement('input');
  frameverinput.id = 'framever';
  frameverinput.placeholder = 'Enter Framework Version';
  const file = document.createElement('label');
  file.append('Upload Model File: ');
  const fileinput = document.createElement('INPUT');
  fileinput.setAttribute("type", "file");
  fileinput.id = 'file';
  div.appendChild(modelname);
  div.appendChild(name);
  div.appendChild(des);
  div.appendChild(desinput);
  div.appendChild(modelframe);
  div.appendChild(select);
  div.appendChild(framename).appendChild(framenameinput);
  div.appendChild(framever);
  div.appendChild(frameverinput);
  div.appendChild(file);
  div.appendChild(fileinput);

  select.onchange = function(){
    var id = (document.getElementById('framework') as HTMLInputElement).value;
    var selectedFrame = models.find((n: { id: string; }) => n.id == id);
    if(selectedFrame.name == 'Other'){
      frameworkName = '';
      framename.style.visibility = "visible";
      framenameinput.style.visibility = 'visible';
    }
    else{
      frameworkName = selectedFrame.name;
      framename.style.visibility = "hidden";
      framenameinput.style.visibility = 'hidden';
    }
  };
  
  fileinput.onchange = function(event){
    const target = event.target as HTMLInputElement;
    fileData = target.files;
  };
  return div;
}
/**
 * Activate the extension.
 *
 * @param app Main application object
 */
function activate(app: JupyterFrontEnd): void {
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}

/**
 * Export the plugin as default.
 */
export default plugin;

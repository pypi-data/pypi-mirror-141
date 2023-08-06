import { IDisposable, DisposableDelegate } from '@lumino/disposable';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { Dialog, showDialog, ToolbarButton } from '@jupyterlab/apputils';

import { DocumentRegistry } from '@jupyterlab/docregistry';
import { Widget } from '@lumino/widgets';
import {
  NotebookPanel,
  INotebookModel,
} from '@jupyterlab/notebook';

let accessToken: any;
var models: any;
let fileData: any;
let dependFile: any;
let time_dur: number;
let time_unit: number;
/**
 * The plugin registration information.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: 'makana-service',
  autoStart: true,
};

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
      fetch('https://makana-app-staging-wa.azurewebsites.net/api/makana/models',{
      method:'GET',
      headers:{
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + data.access_token
      },
      }).then((response) => response.json())
      .then((data) => {
        console.log(data);
          models = data;
        })
      })
      .catch((error) => {
          console.error('Error:', error)
      });
    const modelService = () => {
      showDialog({
        title: "Register New Service",
        body: new SaveWidget(),
        buttons: [Dialog.cancelButton(), saveBtn]
        }).catch((e) => console.log(e));
    };

    const registerService = new ToolbarButton({
      className: 'clear-output-button',
      label: 'Register New Service',
      onClick: modelService,
      tooltip: 'Register a New Service',
    });

    panel.toolbar.insertItem(10, 'registerService', registerService);

    return new DisposableDelegate(() => {
      registerService.dispose();
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
    var serviceName = (document.getElementById('serviceName') as HTMLInputElement).value;
    var description = (document.getElementById('desinput') as HTMLInputElement).value;
    var model = (document.getElementById('model') as HTMLInputElement).value;
    var container = (document.getElementById('container') as HTMLInputElement).value;
    // time_unit = (document.getElementById('number') as HTMLInputElement).value;
    // time_dur = (document.getElementById('idelSelect') as HTMLInputElement).value;
    var serviceForm = new FormData();
    serviceForm.append('id', "");
    serviceForm.append('name', serviceName);
    serviceForm.append('description', description);
    serviceForm.append('modelDefinitionId', model);
    serviceForm.append('containerRunMode', container);
    if(time_unit == 0){
      var timeunit = (document.getElementById('idleTimeUnit') as HTMLInputElement).value;
      console.log(timeunit);
      serviceForm.append('idleTimeUnit', timeunit.toString());
    }
    if(time_dur == 0){
      var timeduration = (document.getElementById('idleTimeDuration') as HTMLInputElement).value;
      console.log(timeduration);
      serviceForm.append('idleTimeDuration', timeduration.toString());
    }
    serviceForm.append('scriptFileName', fileData[0].name);
    serviceForm.append('scriptFileUri', '');
    serviceForm.append('scriptFile', fileData[0]);
    serviceForm.append('dependenciesFileName', dependFile[0].name);
    serviceForm.append('dependenciesFileUri', '');
    serviceForm.append('dependenciesFile', dependFile[0]);
    serviceForm.append('status', "");
    fetch('https://localhost:44350/api/makana/modelservices', {
      method: 'POST',
      headers:{
        'Authorization': 'Bearer ' + accessToken 
      },
      body: serviceForm,
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
  select.setAttribute("id", "model");
  const div = document.createElement('div');
  div.id = 'div';
  div.className = 'form-control';
  console.log("Ohk Changes get");
  const modelname = document.createElement('label');
  modelname.append('Service Name: ');
  const name = document.createElement('input');
  name.setAttribute('class', 'row');
  name.placeholder = 'Enter Service Name';
  name.id = 'serviceName';
  name.style.borderLeftWidth = '5px';
  const des = document.createElement('label');
  des.append('Description: ');
  const desinput = document.createElement('input');
  desinput.id = 'desinput';
  desinput.placeholder = 'Enter description';
  desinput.style.borderLeftWidth = '5px';
  const modelframe = document.createElement('label');
  modelframe.append('Model: ');
  
  models.forEach(function(key: any){
    var option = document.createElement("option");
    option.value = key.id;
    option.text = key.name;
    select.appendChild(option);
  });
  select.setAttribute('class','form-control');
  select.style.borderLeftWidth = '5px';
  const container = document.createElement('label');
  container.append('Container Run Mode: ');
  const conselect = document.createElement('select');
  conselect.id = 'container';
  const continuous = document.createElement('option');
  continuous.value = '0';
  continuous.text = 'Continuous';
  conselect.appendChild(continuous);
  const onDeamnd = document.createElement('option');
  onDeamnd.value = '1';
  onDeamnd.text= 'On Demand';
  conselect.appendChild(onDeamnd);
  conselect.style.borderLeftWidth = '5px';
  const idelDiv = document.createElement('div');
  const idleTIme = document.createElement('label');
  idleTIme.append('Idel Time: ');
  const number = document.createElement('input');
  number.setAttribute("type", "number");
  number.setAttribute("min", "1");
  number.setAttribute("max", "100");
  number.style.borderLeftWidth = '5px';
  number.id = 'idleTimeDuration';
  const idelselect = document.createElement('select');
  idelselect.id = "idleTimeUnit";
  const min = document.createElement('option');
  min.value = '0';
  min.text= 'Minutes';
  const hours = document.createElement('option');
  hours.value = '1';
  hours.text= 'Hours';
  const day = document.createElement('option');
  day.value = '2';
  day.text= 'Days';
  idelselect.style.borderLeftWidth = '5px';
  idelselect.style.inlineSize = 'fit-content';
  idelselect.appendChild(min);
  idelselect.appendChild(hours);
  idelselect.appendChild(day);
  idelDiv.appendChild(idleTIme);
  idelDiv.appendChild(number).appendChild(idelselect);
  const file = document.createElement('label');
  file.append('Script File: ');
  const fileinput = document.createElement('INPUT');
  fileinput.setAttribute("type", "file");
  fileinput.id = 'script';
  fileinput.style.borderLeftWidth = '5px';
  const dependfile = document.createElement('label');
  dependfile.append('Dependencies File: ');
  const dependFileInput = document.createElement('input');
  dependFileInput.setAttribute("type", "file");
  dependFileInput.id = 'dependFile';
  dependFileInput.style.borderLeftWidth = '5px';
  // div.appendChild(nameDiv);
  div.appendChild(modelname);
  div.appendChild(name);
  div.appendChild(des);
  div.appendChild(desinput);
  div.appendChild(modelframe).appendChild(select);
  div.appendChild(container).appendChild(conselect);
  div.appendChild(idelDiv);
  div.appendChild(file);
  div.appendChild(fileinput);
  div.appendChild(dependfile);
  div.appendChild(dependFileInput);
  conselect.onchange = function(){
    var id = (document.getElementById('container') as HTMLInputElement).value;
    if(id != "1"){
      idelDiv.style.visibility = "hidden";
    } else{
      idelDiv.style.visibility = "visible";
      time_unit = 0;
      time_dur = 0;
    }
  };
  
  fileinput.onchange = function(event){
    const target = event.target as HTMLInputElement;
    fileData = target.files;
  };
  dependFileInput.onchange = function(event){
    const target = event.target as HTMLInputElement;
    dependFile = target.files;
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
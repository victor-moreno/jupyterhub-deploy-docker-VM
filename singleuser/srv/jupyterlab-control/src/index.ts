import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter
} from '@jupyterlab/application';

import { Widget } from '@lumino/widgets';

import { ITopBar } from 'jupyterlab-topbar';

import '@jupyterlab/application/style/buttons.css';

import '../style/index.css';

const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-control:plugin',
  autoStart: true,
  requires: [IRouter, ITopBar],
  activate: async (app: JupyterFrontEnd, router: IRouter, topBar: ITopBar) => {
    const control = document.createElement('a');
    control.id = 'control';
    control.innerHTML = 'Control';
    control.addEventListener('click', () => {
      router.navigate('../../home', { hard: true }); });
      
    const widget = new Widget({ node: control });
    widget.addClass('jp-Button-flat');
    topBar.addItem('control-button', widget);
  }
};

export default extension;

/**
* ----------------------------------------------------------------------------
* Copyright (c) 2013 - Damián Avila
* Copyright (c) 2015 - Joshua Cooke Barnes (jcb91)
*
* Distributed under the terms of the Modified BSD License.
*
* A little extension to give Zenmode functionality to the IPython notebook.
* ----------------------------------------------------------------------------
*/

define([
    "jquery",
    "base/js/namespace",
    'base/js/dialog',
], function(
    $,
    IPython,
    dialog,
) {
    "use_strict";
    var modelsResponse;
    var makanaservice = function(){
        var token;
        var settings = {
            "url": "https://localhost:44350/connect/token",
            "method": "POST",
            "timeout": 0,
            "headers": {
              "Content-Type": "application/x-www-form-urlencoded"
            },
            "data": {
              "client_id": "makana_api",
              "grant_type": "client_credentials",
              "scope": "makanaapp_api",
              "client_secret": "TAxhx@9tH(l^MgQ9FWE8}T@NWUT9U)"
            }
          };
          
          $.ajax(settings).done(function (response) {
            token = response.access_token;
          });
        var time_unit;
        var current_dir = $('body').attr('data-notebook-path').split('/').slice(0, -1).join("/");
        var multiselect = $('<option/>').attr('value','multiselect').attr('disabled','').text('-');
        var selected = $('<select/>')
                    .attr('id','modelId')
                    .attr('aria-label', 'combobox, select mdoel framework')
                    .attr('role', 'combobox').addClass('form-control').addClass(multiselect);
        var dialog_body = $('<div/>').append(
                $('<p/>').addClass('save-message')
                    .text('Service Name')
            ).append(
                $('<br/>')
            ).append(
                $('<input/>').attr('type','text').attr('size','25')
                .attr('id', 'service_name')
                .addClass('form-control')
            ).append(
                $('<br/>')
            ).append($('<p/>').addClass('save-message')
            .text('Description')
            ).append(
                $('<br/>')
            ).append(
                $('<input/>').attr('type','text').attr('size','25')
                .attr('id', 'des')
                .addClass('form-control')
            ).append(
                $('<br/>')
            ).append($('<p/>').addClass('save-message')
            .text('Model')
            ).append($('<br/>')
            ).append(selected)
            .append(
                $.each(modelsResponse, function(i, p){
                    selected.append($('<option/>').attr('value',p.id).html(p.name));
                })
            ).append(
                $('<br/>')
            ).append($('<p/>').addClass('save-message')
            .text('Container Run Mode')
            ).append($('<br/>')
            ).append(
                $('<select/>').attr('size','1')
                .attr('id','run_mode')
                .attr('aria-label', 'combobox , select model')
                .attr('role', 'combobox')
                .addClass('form-control select-xs')
                .append($('<option/>').attr('value','0').text('Continuous'))
                .append($('<option/>').attr('value','1').text('On Deamnd'))
                .addClass('form-control')
                .append(multiselect)
            ).append(
                $('<br/>')
            ).append($('<p/>').text('Idel Time:').attr('id','idel')
            ).append(
                $('<input/>').attr('type','number')
                .attr('id', 'time_dur').attr('min','1').attr('max','100')
                .addClass('form-control')
            ).append($('<select/>')
                .attr('id','time_unit')
                .attr('role', 'combobox').addClass('form-control')
                .append($('<option/>').attr('value','0').text('Minutes'))
                .append($('<option/>').attr('value','1').text('Hours'))
                .append($('<option/>').attr('value','2').text('Days'))
            ).append($('<p/>').addClass('save-message')
            .text('Script File')
            ).append(
                $('<br/>')
            ).append(
                $('<input/>').attr('type','file').attr('size','25')
                .attr('id', 'script_file').attr('accept', '.py')
                .addClass('fileinput')
            ).append(
                $('<br/>')
            ).append($('<p/>').addClass('save-message')
            .text('Dependencies File')
            ).append(
                $('<br/>')
            ).append(
                $('<input/>').attr('type','file').attr('size','25')
                .attr('id', 'depen_file').attr('accept', '.txt')
                .addClass('fileinput')
            );

        var d = dialog.modal({
            title: 'New Service',
            body: dialog_body,
            keyboard_manager: IPython.keyboard_manager,
            notebook: IPython.notebook,
            buttons: {
                Cancel: {},
                Save: {
                    class: 'btn-primary',
                    click: function() {
                        
                        var serviceName = d.find('#service_name').val();
                        var des = d.find('#des').val();
                        var modelId = d.find('#modelId').val();
                        var conMode = d.find('#run_mode').val();
                        var scriptFile = d.find('#script_file').keydown(function (event) {});
                        var depenFile = d.find('#depen_file').keydown(function (event) {});
                        time_dur = d.find('#time_dur').val();
                        time_unit = d.find('#time_unit').val();
                        if (!serviceName && !des && !model && !conMode && !scriptFile && !depenFile) {
                            $(".save-message").html(
                                    $("<span>")
                                        .attr("style", "color:red;")
                                        .text($(".save-message").text())
                                );
                            return false;
                        }
                        var formData = new FormData();
                        formData.append('id', "");
                        formData.append('name', serviceName);
                        formData.append('description', des);
                        formData.append('modelDefinitionId', modelId);
                        formData.append('containerRunMode', conMode);
                        if(time_unit){
                            formData.append('idleTimeUnit', time_unit);
                        }
                        if(time_dur){
                            formData.append('idleTimeDuration', time_dur);
                        }
                        formData.append('scriptFileName', scriptFile[0].files[0].name);
                        formData.append('scriptFileUri', null);
                        formData.append('scriptFile', scriptFile[0].files[0]);
                        formData.append('dependenciesFileName', depenFile[0].files[0].name);
                        formData.append('dependenciesFileUri', null);
                        formData.append('dependenciesFile',depenFile[0].files[0]);
                        formData.append('status', "");
                        var settings = {
                            "url": "https://localhost:44350/api/makana/modelservices",
                            "method": "POST",
                            "timeout": 0,
                            "headers": {
                                "Authorization": "Bearer "+ token
                            },
                            "processData": false,
                            "contentType": false,
                            "data": formData
                            };
    
                        $.ajax(settings).done(function (response) {
                            console.log(response);
                        });
                    }
                },
            }
        });
        dialog_body.change(function (){
            var id = d.find('#run_mode').val();
            if (id != 1) {
                d.find('#idel').hide();
                d.find('#time_dur').hide();
                d.find('#time_unit').hide();
              } else {
                d.find('#idel').show();
                d.find('#time_dur').show();
                d.find('#time_unit').show();
                time_dur = d.find('#time_dur').val();
                time_unit = d.find('#time_unit').val();
              }
        })
    };

    var initialize = async function () {
        var settings = {
            "url": "https://makana-app-staging-wa.azurewebsites.net/connect/token",
            "method": "POST",
            "timeout": 0,
            "headers": {
              "Content-Type": "application/x-www-form-urlencoded"
            },
            "data": {
              "client_id": "makana_api",
              "grant_type": "client_credentials",
              "scope": "makanaapp_api",
              "client_secret": "TAxhx@9tH(l^MgQ9FWE8}T@NWUT9U)"
            }
        };
        await $.ajax(settings).done(function (response) {
            var settings = {
                "url": "https://makana-app-staging-wa.azurewebsites.net/api/makana/models",
                "method": "GET",
                "timeout": 0,
                "headers": {
                  "Authorization": "Bearer " + response.access_token,
                  "Content-Type": "application/json"
                },
              };
              $.ajax(settings).done(function (response) {
                modelsResponse = response;
            });
        });
    };

    var load_ipython_extension = async function() {
        $(IPython.toolbar.add_buttons_group([
            IPython.keyboard_manager.actions.register({
                'help'   : 'Makana Service',
                'icon'    : 'fa-empire',
                'handler': makanaservice,
            }, 'model-service', 'makanaservice'),
        ]))
        return await IPython.notebook.config.loaded.then(initialize);
    };

    var extension = {
        load_ipython_extension : load_ipython_extension,
        makanaservice : makanaservice
    };
    return extension;
});

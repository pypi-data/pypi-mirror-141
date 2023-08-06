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
    var modelFrameworkResponse;
    var makanamodel = function() {
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
        var frameName= "";
        var selected = $('<select/>')
                    .attr('id','cell_type')
                    .attr('aria-label', 'combobox, select mdoel framework')
                    .attr('role', 'combobox').addClass('form-control');
        var dialog_body = $('<div/>').append(
                $('<p/>').addClass('save-message').text('Model Name')
                ).append(
                    $('<br/>')
                ).append(
                    $('<input/>').attr('type','text').attr('size','25')
                    .attr('id', 'model_name')
                    .addClass('form-control')
                ).append(
                    $('<br/>')
                ).append($('<p/>').addClass('save-message')
                .text('Description')
                ).append($('<br/>')
                ).append(
                    $('<input/>').attr('type','text').attr('size','25')
                    .attr('id', 'des')
                    .addClass('form-control')
                ).append($('<br/>')
                ).append($('<p/>').addClass('save-message')
                .text('Model Framework')
                ).append($('<br/>')
                ).append(selected)
                .append(
                    $.each(modelFrameworkResponse, function(i, p){
                        selected.append($('<option/>').attr('value',p.id).html(p.name));
                    })
                ).append($('<br/>')
                ).append($('<p/>').attr('id','frame_label').addClass('save-message')
                .text('Framework Name')
                ).append($('<br/>')
                ).append(
                    $('<input/>').attr('type','text').attr('size','25')
                    .attr('id', 'frame_name')
                    .addClass('form-control')
                ).append($('<br/>')
                ).append($('<p/>').addClass('save-message')
                .text('Framework Version')
                ).append($('<br/>')
                ).append(
                    $('<input/>').attr('type','text').attr('size','25')
                    .attr('id', 'frame_ver')
                    .addClass('form-control')
                ).append($('<br/>')
                ).append($('<p/>').addClass('save-message')
                .text('Upload Model File')
                ).append($('<br/>')
                ).append(
                    $('<input/>').attr('type','file')
                    .attr('id', 'model_file')
                );
        
        var d = dialog.modal({
            title: 'Create a New Makana Model',
            body: dialog_body,
            keyboard_manager: IPython.keyboard_manager,
            notebook: IPython.notebook,
            buttons: {
                Cancel: {},
                Save: {
                    class: 'btn-primary',
                    click: function() {
                        var modelName = d.find('#model_name').val();
                        var des = d.find('#des').val();
                        var modelFrameworkId = d.find('#cell_type').val();
                        if(!frameName){
                            frameName = d.find('#frame_name').val();
                        }
                        var frameVer = d.find('#frame_ver').val();
                        var fileData = d.find('#model_file').keydown(function (event) {});
                        if (modelName == "" && des == "" && modelFrameworkId == "" && frameName == "" && frameVer == "" && !fileData[0].files[0]) {
                            $(".save-message").html(
                                $("<span>")
                                    .attr("style", "color:red;")
                                    .text($(".save-message").text())
                                );
                            return false;
                        }
                        const ff = fileData[0].files[0];
                        const fname = fileData[0].files[0].name;
                        var form = new FormData();
                        form.append('id', "");
                        form.append('name', modelName);
                        form.append('description', des);
                        form.append('modelFrameworkId', modelFrameworkId);
                        form.append('frameworkName', frameName);
                        form.append('frameworkVersion', frameVer);
                        form.append('modelFileName', fname);
                        form.append('modelFileUri', "");
                        form.append('modelFile', ff);
                        var settings = {
                        "url": "https://localhost:44350/api/makana/models",
                        "method": "POST",
                        "timeout": 0,
                        "headers": {
                            "Authorization": "Bearer "+ token
                        },
                        "processData": false,
                        "contentType": false,
                        "data": form
                        };
                        $.ajax(settings).done(function (response) {

                        });
                    }
                },
            },
        });
        dialog_body.change(function (){
            var id = d.find('#cell_type').val();
            var selectedValue =modelFrameworkResponse.find(n=> n.id == id);
            if (selectedValue.name != "Other") {
                frameName = selectedValue.name;
                d.find('#frame_label').hide();
                d.find('#frame_name').hide();
              } else {
                frameName = "";
                d.find('#frame_label').show();
                d.find('#frame_name').show();
              }
        })
    }

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
                "url": "https://makana-app-staging-wa.azurewebsites.net/api/makana/modelframeworks",
                "method": "GET",
                "timeout": 0,
                "headers": {
                  "Authorization": "Bearer " + response.access_token,
                  "Content-Type": "application/json"
                },
              };
              $.ajax(settings).done(function (response) {
                modelFrameworkResponse = response;
            });
        });
    }

    var load_ipython_extension = async function() {
        $(IPython.toolbar.add_buttons_group([
            IPython.keyboard_manager.actions.register({
                'help'   : 'Makana Model',
                'icon'    : 'fa-empire',
                'handler': makanamodel,
            }, 'makana-model', 'makanaservice'),
        ]))
        return await IPython.notebook.config.loaded.then(initialize);
    };

    var extension = {
        load_ipython_extension : load_ipython_extension,
        makanamodel : makanamodel
    };
    return extension;
});

import os
import io
from Bio import SeqIO
import time
import iMVP_utils
from iMVP_utils import interactive_functions
# import interactive_functions
import base64
import PIL.Image as Image
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output,State
from dash import callback_context
from flask import Flask

def launch_backend(output_path="./output/"):
    """The function to launch the backend for interactive

    Parameters
    ---------
    output_path: str
        The output directory of the files.
    
    Returns
    ---------
        A Dash App object.
    """
    assets_path = os.path.dirname(iMVP_utils.__file__) + "/assets/"

    server= Flask(__name__)
    app = dash.Dash(name="app1", server=server, assets_folder=assets_path)

    """Run this app with 'python app.py -p port_number and visit http://127.0.0.1:prot_number/ in your web browser.
    (Press CTRL+C to quit)

    """

    if os.path.exists (output_path) == False:
        os.mkdir(output_path)

    def run_iMVP(content, input_parameters):
        """Clustering upload data in fasta format with UMAP and HDBSCAN. 

        Parameters
        ---------
        content: string
            A comma separated string, including type and content of upload file. 
        input_parameters: dict
            A list of reserved parameters for HDBSCAN.
        ---------

        Returns
        ---------
            A Div component: chilren
                A html div of 'processing' information.
            Html stlye: dict
                A style of 'submit-data' button. 
            HDBSCAN_dict: dict
                The results of HDBSCAN.
        """
        nonlocal output_path
        time_start = time.time()
        _, content_string = content.replace(">", "").split(',')
        
        decoded = base64.b64decode(content_string)
        style_submit_button = {'width': '40%'}
    
        df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),sep = "\n", header=None)
        fa_data = pd.concat([df[::2].reset_index(drop=True),df[1::2].reset_index(drop=True)],axis=1)
        fa_data.columns = ['sites','seq']
        # run HDBSACN
        df_HDBSCAN = interactive_functions.run_cluster(fa_data, output_path, input_parameters)
        HDBSCAN_dict = df_HDBSCAN.to_dict()
        
        time_end = time.time()
        
        
        # used_time = round((time_end - time_start)/60,2)
        used_time = time_end - time_start
        if used_time >= 3600:
            used_time = time.strftime("%H hr %M min %S sec", time.gmtime(used_time))    
        elif used_time >= 60:
            used_time = time.strftime("%M min %S sec", time.gmtime(used_time))   
        else:
            used_time = time.strftime("%S sec", time.gmtime(used_time))   
            
        # except Exception as e :
        #     return html.Div([
        #         'There was an error processing this file.'
        #     ]), {'display':'none'}

        return html.Div([html.H3("Finished in {}!".format(used_time)), html.H3('Done !')]), style_submit_button , HDBSCAN_dict

    @app.callback(
        Output('upload_data','children'),
        Input('upload_data','filename')
    )

    def upload_info(filename):  
        if filename is None:
            return html.Div([
                'Drag and Drop or ',html.A('Select Fasta Files')
            ])
        else:
            for file in filename:
                
                return html.Div([
                    html.B('{filename}'.format(filename = file),style={'color':'#ff4777'}),' has been uploaded'
                ])

    @app.callback(
                Output('hdbscan-parameter-list','data'),
                Output('processing_1', 'children'),
                Output('processing_3','children'),
                Output('upload_data', 'style'),
                Output('para-list-div', 'style'),
                Output('upload-div', 'style'),
                Input('submit-button-state', 'n_clicks'),
                [
                State('upload_data', 'contents'), 
                State('exp_len', 'value'), 
                State('n_neighbors', 'value'), 
                State('min_dist', 'value'), 
                State('random_state', 'value'), 
                State('umap_jobs', 'value'), 
                State('umap_init', 'value'), 
                State('densmap', 'value'), 
                State('min_cluster_size', 'value'),
                State('min_samples', 'value'),
                State('cluster_selection_method', 'value'),
                State('cluster_selection_epsilon', 'value'),
                State('hdbscan_jobs', 'value'),
                State('softclustering', 'value'),
                State('weblogo_unit', 'value'),
                State('weblogo_first_index', 'value'),
                ],
                prevent_initial_call=True) 

    def infomation_hide_div(n_clicks,list_of_contents, exp_len, n_neighbors, min_dist, random_state, umap_jobs, umap_init, densmap ,min_cluster_size, min_samples, cluster_selection_method, cluster_selection_epsilon, hdbscan_jobs, softclustering, weblogo_unit, weblogo_first_index):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger the clustering.
            list_of_contents: list
                Contents of upload data.
            exp_len: int
                The expected lengths for the sequences.
            n_neighbors: int
                n_neighbors for UMAP.
            min_dist: int
                min_dist for UMAP.
            random_state: int
                random_state for UMAP.
            umap_jobs: int
                n_jobs for UMAP.
            umap_init: str
                init for UMAP.
            densmap: boolean
                densmap for UMAP.
            min_cluster_size: int
                The parameter of HBDSACN from user.
            min_samples: int
                The parameter of HBDSACN from user.
            cluster_selection_method: string
                The parameter of HBDSACN from user.
            core_dist_n_jobs: int
                The parameter of HBDSACN from user.
            softclustering: bool
                The parameter of HBDSACN from user.
            weblog_unit: str
                The parameter for Weblogo.
            weblog_first_index: str
                The parameter for Weblogo.
        ---------

        Return
        ---------
            hdbscan-parameter-list: dict
                The parameters of HDBSCAN from user.
            processing_1: div object
                The information about data processing.
            processing_3: div object
                The information about data processing.
            upload_data: dict
                A Div style of 'upload_data' to hide the div object.
            para-list-div: dict
                A Div style of 'para-list-div' to hide the div.
            upload-div: dict
                A Div style of 'upload-div' to hide the div.
        """
        dict_parameters = {
            "exp_len": exp_len,
            "n_neighbors": n_neighbors,
            "min_dist": min_dist,
            "random_state": random_state,
            "umap_jobs": umap_jobs,
            "umap_init": umap_init,
            "densmap": densmap,
            "min_cluster_size": min_cluster_size,
            "min_samples": min_samples,
            "cluster_selection_method": cluster_selection_method,
            "cluster_selection_epsilon": cluster_selection_epsilon,
            "hdbscan_jobs": hdbscan_jobs,
            "softclustering": softclustering,
            "weblogo_unit": weblogo_unit,
            "weblogo_first_index": weblogo_first_index,
        }
        
        hide_div_style = {'display': 'none'}
        if list_of_contents is not None:
            for c in list_of_contents:
                return dict_parameters,[html.H3(time.asctime( time.localtime(time.time())))],html.H3('Processing ......',id='process'),hide_div_style,hide_div_style,hide_div_style

    @app.callback(
                Output('processing_2', 'children'),
                Output('submit-data', 'style'),
                Output('cluster-data', 'data'),
                Output('processing_3','style'),
                Output('horizontal_line','style'),
                Input('hdbscan-parameter-list','data'),
            [State('upload_data', 'contents')],
                prevent_initial_call=True)

    def upload_file(parameter_list, list_of_contents):

        """
        Parameters
        ---------
            parameter_list: list
                The parameters of HDBSCAN from user.
            list_of_contents: list
                A content of upload file.

        ---------

        Returns
        ---------
            processing_2: div object
                The information about data processing.
            style: dict
                A style to hide 'submit-data' div object.
            parameters_dict: dict
                The results of clustering with HDBSCAN. 
            hide_info_style: dict
                A style to hide 'processing_2' div object.
            display_hr: dict
                A style to display horizontal line.
        """  
        hide_info_style  = {'display':'none'}
        display_hr = {'display':'inline-block'}
        print(parameter_list)
        if list_of_contents is not None:
            for c in list_of_contents:
                iMVP_out =  run_iMVP(c, parameter_list)
                if len(iMVP_out) == 2:
                    processing_2, style = iMVP_out
                    parameters_dict = None
                else:
                    processing_2, style, parameters_dict = iMVP_out
        
        return processing_2, style, parameters_dict, hide_info_style, display_hr


    @app.callback(
        Output('cluster_figure', 'figure'),
        Output('my-checklist','options'),
        Output('type', 'data'),
        Output('hidden_data','style'),
        Output('submit-button','style'),
        [Input('submit-data','n_clicks'),
        State('cluster-data', 'data')],prevent_initial_call=True
    )

    def cluster_figure(n_clicks, cluster_data):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger clustering.
            cluster_data: dict
                The results of clustering with HDBSCAN.
        ---------

        Returns
        ---------
            cluster_figure:  graph object in plotly
                A graph to display the clusters of HBDSCAN.
            my-checklist: list
                The types of cluster that user choosed.
            type: list
                Types of clusters.
            hidden_data: dict
                A style to hide the div object.
            submit-button: button object
                A style to show the div of button object. 

        """
        dff = pd.DataFrame(cluster_data)
        df = dff.sort_values(by="Cluster", ascending=True)
        type = range(1,max(df['Cluster']) + 1)
        df['Cluster'] = df['Cluster'].astype(str)
        available_type =  list(map(str, type)) 
        df['customdata'] = df.index.values.tolist()
        options = [{'label': i, 'value':i } for i in available_type]
        fig = px.scatter(df,x="X",y="Y",color = "Cluster",custom_data = ["customdata"])
        fig.update_layout( dragmode='lasso', hovermode=False)
        
        return fig, options,available_type,{'display':'inline-block'},{'display':'none'}

    @app.callback(
        Output("my-checklist", "value"),
        Output("all-or-none", "value"),
        Output("select-data","data"),
        [Input("type", 'data'),
        Input("all-or-none", "value"),
        Input("my-checklist", 'value')],
    )

    def select_all_none(option,all_selected, my_selected):
        """
        Parameters
        ---------
            option: list
                Types of all clusters.
            all_selected: list
                When user choose all clusters. 
            my_selected: list 
                Types of clusters that user choosed.

        ---------

        Returns
        ---------
            my-checklist: list
                Types of clusters that user choosed, which show as checklist object.
            all-or-none: list
                Types of all clusters, which show as checklist object.
            select-data: list
                Types of clusters that user choosed, which store as dcc object.

        """
        ctx = callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if input_id == "my-checklist":
            all_selected = ["Select All"] if set(my_selected) == set(option) else []
        else:
            my_selected = option if all_selected else []
        if all_selected != []:
            select_data = option
        else:
            select_data = my_selected

        return my_selected, all_selected, select_data


    @app.callback(
        Output('weblogo','src'),
        Input('cluster_figure', 'selectedData'),
        Input('cluster-data', 'data'),
        Input('select-data','data'),
        Input('hdbscan-parameter-list','data'),
        prevent_initial_call=True
        )

    def draw_weblogo(selected_data,cluster_data,type, parameter_list):
        """
        Parameters
        ---------
            selected_data: dict
                Data selected with lasso or checklist
            cluster_data: dict
                The results of clustering with HDBSCAN. 
            type: list 
                Types of clusters selected from users
        ---------

        Return
        ---------
            weblogo: png
                Weblogo picture in png format.
        ---------
        """
        nonlocal output_path
        if type == [] and selected_data is None:
            return dash.no_update
        else:
            
            df = pd.DataFrame(cluster_data)
            df['Cluster'] = df['Cluster'].astype(str)
            fa_index = []
            if selected_data is None:
                custom = []
                selected_data = {}
                for i in df[df['Cluster'].isin(type) ].index.values.tolist():
                    custom.append({'customdata':[i]})
                selected_data['points'] = custom
            
            for points in selected_data['points']: 
                fa_index.extend(points.get('customdata'))
            
            fasta_name = "{path}/selected_data.fa".format(path=output_path)
            with open(fasta_name, "w") as fasta_out:
                for idx, row in df.loc[fa_index].iterrows():
                    fasta_out.write(">{}\n{}\n".format(idx, row["seq"]))

            png = interactive_functions.draw_logo(fasta_name, parameter_list)
            image = Image.open(io.BytesIO(png))
            img_file = '{path}/weblogo.png'.format(path=output_path)
            image.save(img_file) 
            encode_img = base64.b64encode(open(img_file,'rb').read())
            
            return 'data:image/png;base64,{}'.format(encode_img.decode())

    @app.callback(
        Output("download-text", "data"),
        Input("btn-download-txt", "n_clicks"),
        prevent_initial_call=True)
    def download_fasta(n_clicks):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger download file in fasta format.
        ---------

        Return
        ---------
            download-text: string   
                A fasta format file.
        ---------
        """
        nonlocal output_path
        with open('{path}/selected_data.fa'.format(path=output_path)) as f:
            contents = f.read()
        return dict(content=contents, filename="seleted_data.fa")

    @app.callback(
        Output("download-csv", "data"),
        Input("btn-download-csv", "n_clicks"),
        prevent_initial_call=True)
    def download_csv(n_clicks):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger download CSV file.
        ---------

        Return
        ---------
            download-text: string   
                A fasta format file.
        ---------
        """
        nonlocal output_path
        with open('{path}/all_clusters.csv'.format(path=output_path)) as f:
            contents = f.read()
        return dict(content=contents, filename="all_clusters.csv")

    @app.callback(
        Output("download-png", "data"),   
        Input("btn-download-png", "n_clicks"),
        prevent_initial_call=True
    )
    def download_weblogo(n_clicks):
        nonlocal output_path
        """
        Parameters
        ---------
            n_clicks: int 
                The number of clicks to trigger download weblogo picture.
        ---------

        Return
        ---------
            download-png: png
                A file in png format of weblogo.
        ---------
        """
        return dash.dcc.send_file("{path}/weblogo.png".format(path=output_path))

    app.layout = html.Div([

        html.H1(
                "RNA modification Viewer",
                style = {'textAlign':'center'}),
            
        html.Div([
            html.Div([
                        html.H4('I. Upload data'),
                        dcc.Upload(
                            id = 'upload_data',
                            multiple=True
                        )], 
                        className = "upload",id = 'upload-div', style={'display':'inline-block', "width":"20%"}
                    ),

            html.Div(
                [   html.H4('II. The sequences'),
                    html.Div([
                        "1. Expected lengths of the sequences =",
                        dcc.Input(id='exp_len', type='number', value='21', min='0'),
                        ]),
                    html.H4('III. UMAP parameters'),
                    html.Div([
                        "1. n_neighbors =",
                        dcc.Input(id='n_neighbors', type='number', value='20', min='0'),
                        ]),
                    html.Div([
                        "2. min_dist =", 
                        dcc.Input(id='min_dist', type='number', value='0.01', step='any', min='0', max='1'), 
                         ]),
                    html.Div([
                        "3. random_state =", 
                        dcc.Input(id='random_state', type='number', value='42', min='-2147483648', max='2147483647'), 
                         ]),
                    html.Div([
                        "4. jobs =", 
                        dcc.Input(id='umap_jobs', type='number', value='6'), 
                         ]),
                    html.Div([
                        "5. init =", 
                        dcc.Dropdown(['random', 'spectral'], 'random', id='umap_init'), 
                         ], style={"width":"30%"}),
                    html.Div([
                        "6. DensMAP =", 
                        dcc.Dropdown(['True', 'False'], 'False', id='densmap'), 
                         ], style={"width":"30%"}),
                    
                    html.H4('IV. HBDSCAN parameters'),
                    html.Div([
                        "1. min_cluster_size =",
                        dcc.Input(id='min_cluster_size', type='number', value='100'),
                        ]),
                    html.Div([
                        "2. min_samples =", 
                        dcc.Input(id='min_samples', type='number', value='100'),
                        ]),
                    html.Div([
                        "3. cluster_selection_epsilon =", 
                        dcc.Input(id='cluster_selection_epsilon', type='number', step="any", value='0.0'),
                        ]),
                    html.Div([
                        "4. cluster_selection_method =",
                        dcc.Dropdown(['eom', 'leaf'], 'eom', id='cluster_selection_method')
                        ], style={"width":"30%"}),
                    html.Div([
                        "5. soft clustering =",
                        dcc.Dropdown(['True', 'False'], 'True', id='softclustering')
                        ], style={"width":"30%"}),
                    html.Div([
                        "6. jobs =", 
                        dcc.Input(id='hdbscan_jobs', type='number', value='6'),
                        ]),

                    html.H4('V. Weblogo'),
                    html.Div(["1. Unit =",
                                dcc.Dropdown(['probability', 'bits'], 'probability', id='weblogo_unit'),
                        ], style={"width":"30%"}), 
                    html.Div(["2. First index =",
                                dcc.Input(id='weblogo_first_index', type='number', value='-10'),
                        ]), 

                    html.Div([
                        html.Br(),

                        html.Div([
                                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                            ],
                            className="input",
                            )
                        ]
                    ),
                    
                    ],
                    id="para-list-div",className = "paralist", style={"width":"50%"}
                ),
        ], className="section1",id = 'section1', style={"width":"100%"}),

        html.Div(id = "processing_1"),
        html.Div(id = "processing_2"),
        html.Div(id = "processing_3"),
        html.Div(
            html.Button(
                    id = 'submit-data',
                    n_clicks=0,
                    children='Draw the Figures',
                    style = {'display':'none'}),
            id = 'submit-button'),
        html.Hr(id = "horizontal_line",style={'display':'none'}),
        html.Div([ 
            html.Div([
                html.Div([
                    html.Div(
                    html.Div(
                            [
                                dcc.Checklist(
                                    id="all-or-none",
                                    options=[{"label": "Select All", "value": "Select All"}],
                                    value=[],
                                    labelStyle={"display": "inline-block"},
                                    
                                ),
                                dcc.Checklist(
                                    id="my-checklist",
                                    # options=[{"label": x, "value": x} for x in option],
                                    value=["1"],
                                    labelStyle={"display": "inline-block"},
                                ),
                            ]
                                )

                        ),
                    html.Div(
                        [
                        html.Div([
                            html.Button("Download FASTA", 
                                id = "btn-download-txt",
                                style = {'width': '99%'}
                                )],
                                style={'display':'inline-block'}, 
                                className='three columns' 
                                ),
                        dcc.Download(id = "download-text"),
                        
                        html.Div([
                            html.Button("Download CSV", 
                                id = "btn-download-csv",
                                style = {'width': '99%'}
                                )],
                                style={'display':'inline-block'}, 
                                className='three columns' 
                                ),
                        dcc.Download(id = "download-csv"),
                        
                        html.Div([
                            html.Button("Download LOGO", 
                                id = "btn-download-png",
                                style = {'width': '99%'}
                                )],
                                style={'display':'inline-block'}, 
                                className='three columns'
                                ),
                        dcc.Download(id = "download-png")      
                        ], className='row'
                        ),
                    ]),
                    html.Div(
                            dcc.Graph(
                                    id = 'cluster_figure'),
                            style={'width': '40%','display': 'inline-block'}
                        ),

                    html.Div(
                            html.Img( id = "weblogo",style={'width': '99%'}
                                    ),     
                            style={'width': '50%','display': 'inline-block','position':'relative','bottom':'150px'}),
                    html.Div(
                        dcc.Markdown('''
                            *Usage:*
                                The software encodes the data using one-hot encoding and the dimensionality reduction using **UMAP**. Then, the matrix is clustered using **HDBSCAN** to get all the clusters from the fasta file.Firstly, upload the fasta data of the same length. Then, input the parameters for the clustering with HDBSCAN. After submitting the data, it will take a few minutes for the background to process the data.Finally, you can select clusters by tick checklist, or use a lasso to circle the parts of interest on the cluster plot. That part of data would display by weblogo of base enrichment.
                            ''')
                    )
                    ],
                id = "hidden_data",style={'display':'none'})
                
            ]),
        dcc.Store(id = "cluster-data"),
        dcc.Store(id = "hdbscan-parameter-list"),
        dcc.Store(id = "select-data"),
        dcc.Store(id = "type")

    ])

    return app

if __name__ == "__main__":
    pass
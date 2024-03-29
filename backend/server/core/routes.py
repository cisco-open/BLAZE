from .views import Default,ResetServer,Models,Config,TestDynamicApis,SwaggerConfig
from .model_views import ModelsList,ModelDetail,ModelInitilize,ModelSearch,ModelSummary, ModelActionables, GetFunctionsFromSwaggerData, RunWithFunctions, CallFunction
from .dataset_views import DatasetsList,DatasetFilesList,DatasetFilesDetails, ListMeetingTranscripts



routes_dict = [
    {
        "endpoint": ['/'],
        "resource":Default
    },
    {
        "endpoint": ['/config'],
        "resource":Config
    },
    {
        "endpoint": ['/swagger_config'],
        "resource":SwaggerConfig
    },
    {
        "endpoint": ['/get_model_checklist'],
        "resource":Models
    },
    {
        "endpoint": ['/datasets'],
        "resource":DatasetsList
    },
    {
        "endpoint": ['/datasets/files','/datasets/files/upload','/datasets/files/delete'],
        "resource":DatasetFilesList,
        
    },
    {
        "endpoint": ['/datasets/files/detail'],
        "resource":DatasetFilesDetails
    },
   
    {
        "endpoint": ['/models'],
        "resource":ModelsList
    },
    {
        "endpoint": ['/models/model'],
        "resource":ModelDetail
    },
    {
        "endpoint": ['/models/model/initialize'],
        "resource":ModelInitilize
    },
    {
        "endpoint": ['/search'],
        "resource":ModelSearch
    },
    {
        "endpoint": ['/summary'],
        "resource":ModelSummary
    },
    {
        "endpoint": ['/actionables'],
        "resource":ModelActionables
    },
    {
        "endpoint": ['/functions'],
        "resource":GetFunctionsFromSwaggerData
    },
    {
        "endpoint": ['/run_function'],
        "resource":RunWithFunctions
    },
    {
        "endpoint": ['/call_function'],
        "resource":CallFunction
    },
    {
        "endpoint": ['/list_webex_meeting_transcripts'],
        "resource":ListMeetingTranscripts
    },
    {
        "endpoint": ['/dynamic_query'],
        "resource":TestDynamicApis
    },
 
]
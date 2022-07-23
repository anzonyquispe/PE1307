"""
Model exported as python.
Name : modelo1
Group : 
With QGIS : 32208
"""

# Imports
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


# Modelo 1
class Modelo1(QgsProcessingAlgorithm):

    # Inicio del algoritmo
    def initAlgorithm(self, config=None):

        # Agrega los pasos a la ruta
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model

        # Arma el objeto feedback con 6 pasos
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)

        # Diccionarios para resultados/outputs
        results = {}
        outputs = {}

        ####### Field calculator ########
        # Parametros para field_calculator
        alg_params = {
            'FIELD_LENGTH': 10, # largo del resultado 
            'FIELD_NAME': 'lnm', # variable a generar
            'FIELD_PRECISION': 0, # precision
            'FIELD_TYPE': 2,  # tipo de variable (String)
            'FORMULA': '"NAME_PROP"', # variable a utilizar
            'INPUT': 'menor_a_11_5ba9e026_dc17_4286_a8ed_af859dabd2a4', # Capa input
            'OUTPUT': parameters['Field_calc']
        }

        # Corre fieldcalculator con los parametros de arriba y guarda el output en
        # outputs['FieldCalculator']
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Field_calc']
        results['Field_calc'] = outputs['FieldCalculator']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(1)
        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ####### Fix geometries ########
        # Parametros de Fix geometries
        alg_params = {
            'INPUT': 'langa_74e20f26_bbd5_4e82_83fc_fa18281dced6', # layer de input
            'OUTPUT': parameters['Fix_geo'] # output
        }

        # Corre fixgeometries con los parametros de arriba y guarda el output en
        # outputs['FixGeometries']
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Fix_geo']
        results['Fix_geo'] = outputs['FixGeometries']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(2)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ####### Fix calculator ########
        # Parametros de Fix calculator
        alg_params = {
            'FIELD_LENGTH': 2, # largo del resultado 
            'FIELD_NAME': 'length', # variable a generar
            'FIELD_PRECISION': 0, # precision
            'FIELD_TYPE': 1,  # tipo de variable (Integer)
            'FORMULA': 'length(NAME_PROP)', # variable a utilizar
            'INPUT': 'Incremented_004eb652_3334_4870_830c_dd457f831645', # Capa input
            'OUTPUT': parameters['Length']
        }

        # Corre fieldcalculator con los parametros de arriba y guarda el output en
        # outputs['FieldCalculator']
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Field_calc']
        results['Length'] = outputs['FieldCalculator']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(3)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ####### Feature filter ########
        # Parametros de Feature filter
        alg_params = {
            'INPUT': 'Calculated_9884987f_204b_471c_9c79_ab515e98fee9', # layer de input
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11'] # output
        }

        # Corre featurefilter con los parametros de arriba y guarda el output en
        # outputs['FeatureFilter']
        outputs['FeatureFilter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Output_menor_a_11']
        results['Output_menor_a_11'] = outputs['FeatureFilter']['OUTPUT_menor_a_11']

        # Pasa al siguiente step
        feedback.setCurrentStep(4)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ####### Drop field(s) ########
        # Parametros de Drop field(s)
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'], # Columnas a dropear
            'INPUT': 'Calculated_ffcf3c42_9e18_46e2_ac4d_d3f77e81b1e6', # layer de input
            'OUTPUT': parameters['Wldsout'] # output
        }

        # Corre dropfields con los parametros de arriba y guarda el output en
        # outputs['DropFields']
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Wldsout']
        results['Wldsout'] = outputs['DropFields']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(5)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ####### Add autoincremental field ########
        # Parametros de Add autoincremental field
        alg_params = {
            'FIELD_NAME': 'GID',  # variable a generar
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometries']['OUTPUT'], # el input es el output de FixGeometries
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id'] # output
        }

        # Corre Add autoincremental field con los parametros de arriba y guarda el output en
        # outputs['AddAutoincrementalField']
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Autoinc_id']
        results['Autoinc_id'] = outputs['AddAutoincrementalField']['OUTPUT']
        return results


    #### Definicion de parámetros generales del modelo ####
    
     # Nombre del modelo
    def name(self):
        return 'modelo1'

    # Nombre visible del modelo
    def displayName(self):
        return 'modelo1'

    # Grupo
    def group(self):
        return ''

    # ID del grupo
    def groupId(self):
        return ''

    # Función para crear instancia
    def createInstance(self):
        return Modelo1()

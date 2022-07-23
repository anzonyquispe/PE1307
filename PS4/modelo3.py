"""
Model exported as python.
Name : modelo3
Group : 
With QGIS : 32208
"""

# Imports
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


# Modelo 3
class Modelo3(QgsProcessingAlgorithm):

    # Inicializacion del algoritmo
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    # Definicion del algoritmo
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model

        # Creacion del objeto feedback
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)

        # Creacion de diccionarios de resultados/outputs
        results = {}
        outputs = {}

        ####### Fix geometries ########
        # Parametros de Fix geometries
        alg_params = {
            'INPUT': 'ne_10m_admin_0_countries_541ea769_f103_4ed6_b179_6d7a688f9e49', # layer de input
            'OUTPUT': parameters['Fixgeo_3'] # output
        }

        # Corre fixgeometries con los parametros de arriba y guarda el output en
        # outputs['FixGeometries']
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Fix_geo']
        results['Fixgeo_3'] = outputs['FixGeometries']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(1)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ####### Drop field(s) ########
        # Parametros de Drop field(s)
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],  # Columnas a dropear
            'INPUT': 'Fixed_geometries_2f0e54f0_3e9d_4f80_b5e0_b0f166d6f46d', # layer de input
            'OUTPUT': parameters['Drop_fields_3'] # output
        }

        # Corre dropfields con los parametros de arriba y guarda el output en
        # outputs['DropFields']
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Drop_fields_3'] 
        results['Drop_fields_3'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        ######## Zonal statistics ##########
        # Parametros de Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'landq',  # nombre de la columna
            'INPUT': 'Remaining_fields_3f2cce0a_2c9f_471b_ae7c_f2a87666fe5f', # layer de input
            'INPUT_RASTER': 'landquality_5175b578_c100_4e69_a41a_f2e7a454f995', # raster de input
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Landq'] # output
        }

        # Corre fieldcalculator con los parametros de arriba y guarda el output en
        # outputs['ZonalStatistics']
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['ZonalStatistics']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(3)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ######## Zonal statistics ##########
        # Parametros de Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'pop1800', # nombre de la columna
            'INPUT': 'Zonal_Statistics_7df8b8de_2812_4fc4_8717_4222f3b9553c', # layer de input
            'INPUT_RASTER': 'popd_1800AD_da5520b9_affe_45d7_9558_752f6602c9db', # raster de input
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1800'] # output
        }

        # Corre fieldcalculator con los parametros de arriba y guarda el output en
        # outputs['ZonalStatistics']
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
 
         # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Pop1800']
        results['Pop1800'] = outputs['ZonalStatistics']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(4)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ######## Zonal statistics ##########
        # Parametros de Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'pop1900', # nombre de la columna
            'INPUT': 'Zonal_Statistics_e1475d9c_8fae_42ee_9561_3935f8d08e33', # layer de input
            'INPUT_RASTER': 'popd_1900AD_98c46a34_f201_4f8f_99cb_c8f629036a84', # raster de input
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1900'] # output
        }

        # Corre fieldcalculator con los parametros de arriba y guarda el output en
        # outputs['ZonalStatistics']
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Pop1900']
        results['Pop1900'] = outputs['ZonalStatistics']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(5)
        
        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ######## Zonal statistics ##########
        # Parametros de Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'pop2000',  # nombre de la columna
            'INPUT': 'Zonal_Statistics_e03e6912_0cde_4047_8690_ec51bf49d644', # layer de input
            'INPUT_RASTER': 'popd_2000AD_8dd62e86_e8bb_4c6f_886e_ed9d839b41d9', # raster de input
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop2000'] # output
        }

        # Corre fieldcalculator con los parametros de arriba y guarda el output en
        # outputs['ZonalStatistics']
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma el ['OUTPUT'] de lo de arriba y lo guarda en results['Pop2000']
        results['Pop2000'] = outputs['ZonalStatistics']['OUTPUT']

        # Pasa al siguiente step
        feedback.setCurrentStep(6)

        # Frena el proceso si se canceló
        if feedback.isCanceled():
            return {}

        ######## Save vector features to file ##########
        # Parametros de Save vector features to file
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Zonal_Statistics_ea0b85bc_b26d_4bdc_984d_1e3a563d1a39',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/estef/Desktop/San Andrés/2022/2do trimestre/Herramientas computacionales para investigación/Tarea 4/output/raster_stats.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }

        # Corre dropfields con los parametros de arriba y guarda el output en
        # outputs['SaveVectorFeaturesToFile']
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Devuelve el diccionario results
        return results

    #### Definicion de parámetros generales del modelo ####
    
    # Nombre del modelo
    def name(self):
        return 'modelo3'

    # Nombre visible del modelo
    def displayName(self):
        return 'modelo3'

    # Grupo
    def group(self):
        return ''

    # ID del grupo
    def groupId(self):
        return ''

    # Función para crear instancia
    def createInstance(self):
        return Modelo3()

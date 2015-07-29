from PySide import QtGui
from PySide import QtCore
import maya.OpenMayaUI as mui
import shiboken
import maya.cmds as cmds
#from mVray import vrayObjectProperties as vop
from mVray import vrayFrameBuffers as vfb
import yaml


def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    

class UtilityToolBoxUI(QtGui.QDialog):
    
    def __init__(self, parent=getMayaWindow()):
        super(UtilityToolBoxUI, self).__init__(parent)
        
        self.setWindowTitle("Utility Toolbox")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed
        
        self.createLayout() # runs def createLayout
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        self.setMinimumHeight(650)
        self.setMinimumWidth(750)
        layout.setSpacing(0)
        
        ########### catch all checkboxes here ################
        self.cbButtonList = {}
        
        #################### top frame ##############################################
        
        self.top_frame = QtGui.QFrame()
        self.top_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.top_frame)
        
        self.top_frame.setLayout(QtGui.QHBoxLayout())
        
        tl = FrameLabel("mask_label", "LightMtls", self.top_frame)
        
        tl.frameLabelVarName.mouseReleaseEvent = self.topToggle
        
        topList = ["Red", "Green", "Blue", "White", "Black"]
        
        self.topListCheckBox = {}
        
        for x in topList:
            cb = UtilCreateCheckBox(x, x, self.top_frame)
            self.topListCheckBox[x] = cb.buttonVarName
            
        self.cbButtonList.update(self.topListCheckBox)
        
        ####################### middle top frame #################################
        
        self.middleTop_frame = QtGui.QFrame()
        self.middleTop_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.middleTop_frame)
        
        self.middleTop_frame.setLayout(QtGui.QHBoxLayout())
        
        mtl = FrameLabel("RE_label", "RenderElem", self.middleTop_frame)
        
        mtl.frameLabelVarName.mouseReleaseEvent = self.midTopToggle
        
        middleTopList = ["Shadow", "Contact_Shadow", "Fresnel", "Reflection_Occ"]
        
        self.midTopListCheckBox = {}
        
        for x in middleTopList:
            cb = UtilCreateCheckBox(x, x, self.middleTop_frame)
            self.midTopListCheckBox[x] = cb.buttonVarName
            
        self.cbButtonList.update(self.midTopListCheckBox)
            
        ##########################  middle bottom frame ##########################################
        
        self.middleBot_frame = QtGui.QFrame()
        self.middleBot_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.middleBot_frame)
        
        self.middleBot_frame.setLayout(QtGui.QHBoxLayout())
        
        mbl = FrameLabel("Shader_label", "Shaders", self.middleBot_frame)
        
        mbl.frameLabelVarName.mouseReleaseEvent = self.midBotToggle
        
        middleBotList = ["Shadow_Catcher", "Plate_Projection", "Reflection_Catcher"]
        
        self.midBotListCheckBox = {}
        
        for x in middleBotList:
            cb = UtilCreateCheckBox(x, x, self.middleBot_frame)
            self.midBotListCheckBox[x] = cb.buttonVarName
       
        self.cbButtonList.update(self.midBotListCheckBox)
             
        ############################ bottom frame ##########################################
        
        self.bottom_frame = QtGui.QFrame()
        self.bottom_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.bottom_frame)

        self.bottom_frame.setLayout(QtGui.QHBoxLayout())
        
        bl = FrameLabel("Util_label", "Utilities", self.bottom_frame)
        
        bl.frameLabelVarName.mouseReleaseEvent = self.bottomToggle
        
        bottomList = ["Ref_Spheres"]
        
        self.bottomListCheckBox = {}
               
        for x in bottomList:
            cb = UtilCreateCheckBox(x, x, self.bottom_frame)
            self.bottomListCheckBox[x] = cb.buttonVarName
            
        self.cbButtonList.update(self.bottomListCheckBox)     
                    
        ######################### Un/Check All buttons ##################################################
        
        allCheckLayout = QtGui.QHBoxLayout()
        layout.addLayout(allCheckLayout)
        
        self.checkAll_button = QtGui.QPushButton("Check All")
        allCheckLayout.layout().addWidget(self.checkAll_button)
        self.checkAll_button.clicked.connect(self.checkAllFunction)
        
        
        self.checkNone_button = QtGui.QPushButton("Check None")
        allCheckLayout.layout().addWidget(self.checkNone_button)
        self.checkNone_button.clicked.connect(self.checkNoneFunction)
                       
        
        ####################### Import button #####################################################
        
        self.import_button = QtGui.QPushButton("Import")
        layout.addWidget(self.import_button)
        self.import_button.setMinimumHeight(50)
        
        self.import_button.clicked.connect(self.importButtonFunction)
                
        ####################### Output Window ####################################################
        
        self.outWindow = QtGui.QTextEdit()
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(250)
        
        ############################################################################################
        
        
        self.setLayout(layout) # add main layout itself to this dialog
        
        
    def importButtonFunction(self):
        
        cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
        if cmds.pluginInfo('vrayformaya', q=True, loaded=True) == False:
            cmds.loadPlugin('vrayformaya', qt=True)
            
        output = []
        warningSphere = []
        warningPlate = []
        
        shotCam = 'shotcam1:shot_camera'   
                 
        for x,y in self.cbButtonList.iteritems():
            
            if x == "Red" and y.isChecked() == True:
                CreateRGBLightMaterials('RED',1,0,0)
                output.append("Created Red VRay Light Material")
                
            if x == "Green" and y.isChecked() == True:
                CreateRGBLightMaterials('GREEN',0,1,0)
                output.append("Created Green VRay Light Material")
                              
            if x == "Blue" and y.isChecked() == True:
                CreateRGBLightMaterials('BLUE',0,0,1)
                output.append("Created Blue VRay Light Material")
                
            if x == "White" and y.isChecked() == True:
                CreateRGBLightMaterials('WHITE',1,1,1)
                output.append("Created White VRay Light Material")
                                
            if x == "Black" and y.isChecked() == True:
                CreateRGBLightMaterials('BLACK',0,0,0)
                output.append("Created Black VRay Light Material")
                
            if x == "Shadow" and y.isChecked() == True:
                CreateRenderElements('shadow')
                output.append("Created Matte Shadow Render Element")
                
            if x == "Contact_Shadow" and y.isChecked() == True:
                CreateCatchers('contact_shadow')
                CreateRenderElements('contactShadow')
                output.append("Created Contact Shadow Render Element")
                output.append("Created Conatct Shadow VRay Dirt Texture")
                                
            if x == "Reflection_Occ" and y.isChecked() == True:
                CreateCatchers('reflection')
                CreateRenderElements('refl_occ')
                output.append("Created Reflection Occlusion VRay Dirt Texture")
                output.append("Created Refleection Occlusion Render Element")               
                                                      
            if x == "Fresnel" and y.isChecked() == True:
                CreateRenderElements('fresnel')
                output.append("Created VRay Frensel Utility")
                output.append("Created Fresnel Render Element")
                        
            if x == "Shadow_Catcher" and y.isChecked() == True:
                CreateCatchers('shadow')
                output.append("Created Shadow Catcher Vray Mtl")
                
            if x == "Plate_Projection" and y.isChecked() == True:
                PlateProject()
                output.append("Created Plate Projection Shader")
                if not cmds.objExists(shotCam): 
                   warningPlate.append("Could not link plate projection node to shotcam. Shotcam does not exist.")
          
            if x == "Reflection_Catcher" and y.isChecked() == True:
                CreateCatchers('reflection')
                output.append("Created Reflection Catcher Vray Mtl")
                 
            if x == "Ref_Spheres" and y.isChecked() == True:
                CreateRefSphere()
                output.append("Created Reference Spheres and Color Chart")
                if not cmds.objExists(shotCam): 
                   warningSphere.append("Could not position and constrain to shotcam. Shotcam does not exist.")
        
                
        conformOutput = '\n'.join(output) ## reformats output list
        conformSphereWarn = '\n'.join(warningSphere) ## reformats output list
        conformPlateWarn = '\n'.join(warningPlate) ## reformats output list
                
        #conformWarn = "<font color=red>" + '\n'.join(warningStuff) + "</font>" ## reformats warning list
        warningSphereOut = "<font color=red>" + conformSphereWarn + "</font>" ## turn that string red
        warningPlateOut = "<font color=red>" + conformPlateWarn + "</font>" ## turn that string red
        
        self.outWindow.setText(conformOutput) ## prints output in output box
        self.outWindow.append(warningSphereOut) ## prints warnings in output box 
        self.outWindow.append(warningPlateOut) ## prints warnings in output box         
    
    def checkAllFunction(self): ## Check all Button
        for x,y in self.cbButtonList.iteritems():
            y.setChecked(True)
        
    def checkNoneFunction(self): ## Check None Button
        for x,y in self.cbButtonList.iteritems():
            y.setChecked(False)

    def topToggle(self, event): ## Top list CB toggle
        flipRow(self.topListCheckBox)        

    def midTopToggle(self, event): ## midTop list CB toggle
        flipRow(self.midTopListCheckBox) 
        
    def midBotToggle(self, event): ## midBot list CB toggle
        flipRow(self.midBotListCheckBox)  

    def bottomToggle(self, event): ## Bottom list CB toggle
        flipRow(self.bottomListCheckBox)             
        


def flipRow(whichList): ## toggle row of checkboxes if you click on the label
    if whichList.values()[0].isChecked() == True:
        for x,y in whichList.iteritems():
            y.setChecked(False)
    else:
        for x,y in whichList.iteritems():
            y.setChecked(True)  

class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame):
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)

        
class FrameLabel(object):
    def __init__(self, frameLabelVarName, frameLabelName, frame):
        
        #self.frameLabelVarName = frameLabelVarName
        # frameLabelVarName = the frame creation variable name
        self.frameLabelName = frameLabelName
        # frameLabelName = the name of the label on the frame
        self.frame = frame
        # frame = which frame it will land in
        
        self.frameLabelVarName = QtGui.QLabel(frameLabelName)
        frame.layout().addWidget(self.frameLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.frameLabelVarName.setFont(font)       
        
if __name__ == "__main__":
    
    # will try and close the ui if it exists
    try:
        ui.close()
    except:
        pass
        
    ui = UtilityToolBoxUI()
    ui.show()


########################################################################
############################### Back End ###############################
########################################################################


class CreateRGBLightMaterials(object):        
    def __init__(self, shaderName, R, G, B):
        
        self.shaderName = shaderName
        self.R = R
        self.G = G
        self.B = B
        
        if not cmds.objExists(shaderName):
            mtlName = cmds.shadingNode('VRayLightMtl', asShader=True, name=shaderName)
            cmds.setAttr('%s.color' % (mtlName), R,G,B, type='double3')
            cmds.setAttr('%s.emitOnBackSide' % (mtlName), 1)
        else:
            mtlName = cmds.ls(shaderName)[0]

## example creation ##    
## createRedShader = CreateRGBLightMaterials('RED',1,0,0)
## createRedShader = CreateRGBLightMaterials('GREEN',0,1,0)
## createRedShader = CreateRGBLightMaterials('BLUE',0,0,1)
## createRedShader = CreateRGBLightMaterials('WHITE',1,1,1)
## createRedShader = CreateRGBLightMaterials('BLACK',0,0,0)

class CreateCatchers(object):    
    def __init__(self, type):
        self.type = type
        ## type meaning 'shadow' or 'reflection' catcher
        
        if type.lower() == 'shadow':
            if not cmds.objExists('SHADOW_CATCHER'):
                shdCatcher = cmds.shadingNode('VRayMtl', asShader=True, name='SHADOW_CATCHER')
                cmds.setAttr('%s.reflectionColorAmount' % (shdCatcher), 0)
                cmds.setAttr('%s.diffuseColorAmount' % (shdCatcher), 1)
                cmds.setAttr('%s.brdfType' % (shdCatcher), 0)
                cmds.setAttr('%s.useFresnel' % (shdCatcher), 0)
            ## creates shadow catching VRayMtl
            
        if type.lower() == 'contact_shadow':           
            if not cmds.objExists('CONTACT_SHADOW_CATCHER'):
                contactShadCatcher = cmds.shadingNode('VRayDirt', asTexture=True, name='CONTACT_SHADOW_CATCHER')
                cmds.setAttr('%s.blackColor' % (contactShadCatcher), 1,1,1, type='double3')
                cmds.setAttr('%s.whiteColor' % (contactShadCatcher), 0,0,0, type='double3')
                cmds.setAttr('%s.radius' % (contactShadCatcher), 10)
                cmds.setAttr('%s.ignoreSelfOcclusion' % (contactShadCatcher), 1)
                cmds.setAttr('%s.resultAffectInclusive' % (contactShadCatcher), 0)
             ## creates VrayDirt used for ambient occlusion
        
        elif type.lower() == 'reflection':
                if not cmds.objExists('REFL_CATCHER'):
                    mirrorMtl = cmds.shadingNode('VRayMtl', asShader=True, name='REFL_CATCHER')
                    cmds.setAttr('%s.color' % (mirrorMtl), 0,0,0, type='double3')
                    cmds.setAttr('%s.reflectionColor' % (mirrorMtl), 1,1,1, type='double3')
                    cmds.setAttr('%s.reflectionColorAmount' % (mirrorMtl), 1)
                    cmds.setAttr('%s.diffuseColorAmount' % (mirrorMtl), 0)
                    cmds.setAttr('%s.useFresnel' % (mirrorMtl), 0)
                    mirrorOccl = cmds.shadingNode('VRayDirt', asTexture=True, name='MIRROR_REFLOCC')
                    cmds.setAttr('%s.blackColor' % (mirrorOccl), 1,1,1, type='double3')
                    cmds.setAttr('%s.whiteColor' % (mirrorOccl), 0,0,0, type='double3')
                    cmds.setAttr('%s.radius' % (mirrorOccl), 1000)
                    cmds.setAttr('%s.occlusionMode' % (mirrorOccl), 2)
                    cmds.connectAttr('%s.outColor' % (mirrorOccl), '%s.reflectionColor' % (mirrorMtl))
                    cmds.connectAttr('%s.reflectionGlossiness' % (mirrorMtl), '%s.glossiness' % (mirrorOccl))          
                    mkbrdfTypeOffset = cmds.shadingNode('plusMinusAverage', asUtility=True, name='brdfOffset')
                    cmds.connectAttr('%s.brdfType' % (mirrorMtl), '%s.input1D[0]' % (mkbrdfTypeOffset))
                    cmds.setAttr('%s.input1D[1]' % (mkbrdfTypeOffset), 1)
                    cmds.connectAttr('%s.output1D' % (mkbrdfTypeOffset), '%s.occlusionMode' % (mirrorOccl))
                    cmds.connectAttr('%s.reflectionSubdivs' % (mirrorMtl), '%s.subdivs' % (mirrorOccl))
                ## creates relfection catching VrayMtl and VRay dirt for an RO

## example creation ##    
## createShadowCatcher = CreateCatchers('shadow') 
## createReflectionCatcher = CreateCatchers('reflection') 

class CreateRenderElements(object):
    def __init__(self,type):
        
        self.type = type
        
        if type.lower() == 'shadow':
            if not cmds.objExists('vrayRE_MatteShadow'):
                vfb.matteShadow('vrayRE_MatteShadow', enabled=False)
            ## creates cast shadow render element
            
        if type.lower() == 'contactshadow':
            if not cmds.objExists('vrayRE_ContactShadow'):
                if cmds.objExists('CONTACT_SHADOW_CATCHER'):
                    vfb.extraTex('vrayRE_ContactShadow', 'CONTACT_SHADOW_CATCHER', explicit_channel='contactShadow', enabled=False)
            ## creates contact shadow render element
            
        if type.lower() == 'fresnel':       
            if not cmds.objExists('vrayRE_Fresnel'):
                createFresnel = cmds.shadingNode('VRayFresnel', asTexture=True, name='VrayFresnel')
                createFresnelTwoD = cmds.shadingNode('place2dTexture', asUtility=True, name='place2dFresnel')
                cmds.connectAttr('%s.outUV' % (createFresnelTwoD), '%s.uvCoord' % (createFresnel))
                cmds.connectAttr('%s.outUvFilterSize' % (createFresnelTwoD), '%s.uvFilterSize' % (createFresnel))
                vfb.extraTex('vrayRE_Fresnel', 'VrayFresnel', explicit_channel='fresnel', enabled=False)
            ## creates fresnel render element
            
        if type.lower() == 'refl_occ':
            if not cmds.objExists('vrayRE_reflectionOcclusion'):
                if cmds.objExists('MIRROR_REFLOCC'):
                    vfb.extraTex('vrayRE_reflectionOcclusion', 'MIRROR_REFLOCC', explicit_channel='reflectionOcclusion', enabled=False)
            ## creates contact shadow render element
                
## example creation ##   
## createShadowRE = CreateRenderElements('shadow')
## createShadowRE = CreateRenderElements('contactShadow')
## createFresnelRE = CreateRenderElements('fresnel')  
   
class PlateProject(object):    
    def __init__(self):
    
        projectCam = 'shotcam1:shot_camera'
        if not cmds.objExists('plateProject'):
            projShader = cmds.shadingNode('VRayLightMtl', asShader=True, name='plateProject')
            cmds.setAttr('%s.emitOnBackSide' % (projShader), 1)
            ## creates shader
            
            plateTexture = cmds.shadingNode('file', asTexture=True, name='plateTexture')
            cmds.setAttr('%s.defaultColor' % (plateTexture), 0,0,0, type='double3')
            cmds.setAttr('%s.useFrameExtension' % (plateTexture), 1)
            ## creates texture node
            
            fileProject = cmds.shadingNode('projection', asTexture=True, name='projectNodePlate') 
            cmds.setAttr('%s.projType' % (fileProject), 8)
            cmds.setAttr('%s.fitType' % (fileProject), 0)
            cmds.setAttr('%s.fitFill' % (fileProject), 1)
            cmds.setAttr('%s.defaultColor' % (fileProject), 0,0,0, type='double3')
            ## creates projection node
            
            twoD = cmds.shadingNode('place2dTexture', asUtility=True, name='PlatePlace2d')
            cmds.setAttr('%s.wrapU' % (twoD), 0)
            cmds.setAttr('%s.wrapV' % (twoD), 0)
            ## creates place2D for plate texture
            
            threeD = cmds.shadingNode('place3dTexture', asUtility=True, name='PlatePlace3d')
            ## creates place3D for camera
            
            cmds.connectAttr('%s.outColor' % (fileProject), '%s.color' % (projShader))
            cmds.connectAttr('%s.outColor' % (plateTexture), '%s.image' % (fileProject))
            cmds.connectAttr('%s.worldInverseMatrix' % (threeD), '%s.placementMatrix' % (fileProject))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityR' % (projShader))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityG' % (projShader))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityB' % (projShader))
            ## connects texture, alpha, shader, projection, and 3D placement
                
            place2DConnections = ('coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV',
                                  'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne')                          
            for x in place2DConnections:
                cmds.connectAttr('%s.%s' % (twoD, x), '%s.%s' % (plateTexture, x))               
            cmds.connectAttr('%s.outUV' % (twoD), '%s.uv' % (plateTexture))
            cmds.connectAttr('%s.outUvFilterSize' % (twoD), '%s.uvFilterSize' % (plateTexture))
            ## connects place2D for plate texture
                
            if cmds.objExists(projectCam):
                cmds.connectAttr('%s' % (projectCam) + 'Shape.message', '%s.linkedCamera' % (fileProject), f=True)
            ## connects shotcam to the proj cam if it exists

## example creation ##   
## createPlateProject = PlateProject()  
  
class CreateRefSphere(object):    
    def __init__(self):
        
        
        if not cmds.objExists('greyBallShader'):
            diffShader = cmds.shadingNode('VRayMtl', asShader=True, name='greyBallShader')
            diffShaderSG = cmds.sets(name = 'greyBallSG', renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (diffShader) ,'%s.surfaceShader' % (diffShaderSG))
            cmds.setAttr('%s.useFresnel' % (diffShader), 0)
            cmds.setAttr('%s.color' % (diffShader),  0.18,0.18,0.18, type='double3')
            ## creates and assigns grey ball shader    
        
        if not cmds.objExists('greyBall'):
            diffBall = cmds.polySphere(name='greyBall', r=2.5)
            cmds.setAttr('%s.translateY' % (diffBall[0]), 6)
            cmds.delete(diffBall, ch=True)
            ## creates grey ball geo
        
            cmds.sets(diffBall[0], e=True, forceElement='greyBallSG')
            ## assigns  grey ball shader to geo
        
        if not cmds.objExists('chromeBallShader'):
            refShader = cmds.shadingNode('VRayMtl', asShader=True, name='chromeBallShader')
            refShaderSG = cmds.sets(name = 'chromeBallSG', renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (refShader) ,'%s.surfaceShader' % (refShaderSG))
            cmds.setAttr('%s.useFresnel' % (refShader), 0)
            cmds.setAttr('%s.color' % (refShader),  0, 0, 0, type='double3')
            cmds.setAttr('%s.reflectionColor' % (refShader),  1, 1, 1, type='double3')
            cmds.setAttr('%s.diffuseColorAmount' % (refShader),  0)
            cmds.setAttr('%s.reflectionsMaxDepth' % (refShader),  2)
            ## creates chrome ball shader
                
        if not cmds.objExists('chromeBall'):    
            refBall = cmds.polySphere(name='chromeBall', r=2.5)
            cmds.delete(refBall, ch=True)  
            ## creates chrome ball geo
            
            cmds.sets(refBall[0], e=True, forceElement='chromeBallSG')
            ## assigns chrome ball shader to geo        

    
        colorChartTexturePath = '/jobs/asset_library/sequences/assets/common/pub/hdr_library/ColorChecker_linear_from_Avg_16bit.exr'
        ## color chart texture path
        
        
        if not cmds.objExists('colorChartShader'):
            chartShader = cmds.shadingNode('VRayLightMtl', asShader=True, name='colorChartShader')
            chartShaderSG = cmds.sets(name = 'chartShaderSG', renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (chartShader) ,'%s.surfaceShader' % (chartShaderSG))
            cmds.setAttr('%s.emitOnBackSide' % (chartShader), 1)

            ## creates color chart VrayLightMtl
        
        if not cmds.objExists('colorChart'):    
            colorChart =  cmds.polyPlane(name='colorChart', h=5,w=5,sx=1,sy=1)
            cmds.setAttr('%s.translate' % (colorChart[0]), 7,3,0)
            cmds.setAttr('%s.rotateX' % (colorChart[0]), 90)
            ## creates color chart geo
            
            cmds.sets(colorChart[0], e=True, forceElement='chartShaderSG')
            ## assigns shader
        
        
        if not cmds.objExists('chartTexture'):
            chartTexture = cmds.shadingNode('file', asTexture=True, name='chartTexture')
            chartTwoD = cmds.shadingNode('place2dTexture', asUtility=True, name='chartPlace2d')    
            chart2DConnections = ('coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV',
                                  'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne')                          
            for x in chart2DConnections:
                cmds.connectAttr('%s.%s' % (chartTwoD, x), '%s.%s' % (chartTexture, x))               
            cmds.connectAttr('%s.outUV' % (chartTwoD), '%s.uv' % (chartTexture))
            cmds.connectAttr('%s.outUvFilterSize' % (chartTwoD), '%s.uvFilterSize' % (chartTexture))
            cmds.connectAttr('%s.outColor' % (chartTexture), '%s.color' % (chartShader))
            ## creates and connects file texture node
            
            cmds.setAttr('%s.fileTextureName' % (chartTexture), colorChartTexturePath, type='string')
            ############ So dumb but I can't get the file tetxture path to fully eval without selecting the file node ###################
            cmds.select(chartTexture, r=True)
            ## feeds in colro chart texture path
        
        if not cmds.objExists('RefSphere_GRP'):
            refSetupGroupName = 'RefSphere_GRP'
            refSetupTransGroup = 'TranslateThis'
            refSetupGroupMembers = (colorChart[0], refBall[0], diffBall[0])
            translateGroup = cmds.group(refSetupGroupMembers, name=refSetupTransGroup)

            refSetupGroup = cmds.group(translateGroup, name=refSetupGroupName)
            shotCam = 'shotcam1:shot_camera'
            if cmds.objExists(shotCam):
                cmds.parentConstraint(shotCam, refSetupGroup, mo=False)
                cmds.setAttr('%s.translate' % (translateGroup), -50, -25, -150)
            ## creates groups and constrains to camera

## example creation ##   
## createRefSpheres = CreateRefSphere()


















    

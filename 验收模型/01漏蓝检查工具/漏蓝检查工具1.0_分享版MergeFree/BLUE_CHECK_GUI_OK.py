#coding=utf-8
import arcpy
import os
import os.path
inWorkspace = arcpy.GetParameterAsText(0)  #输入英文城市名文件所在路径，下含已转好的DAE_SHP文件夹 D:\
#inWorkspace = "D:\\PythonCode_inWork\\09DAE_SHP_Check\\PROCESS\\DATA\\YANGZHOU"
arcpy.AddMessage(inWorkspace)

#城市名自动获取
city = os.path.split(inWorkspace)[-1]

###_H合并Tile
##shps_dir = inWorkspace + "\\DAE_SHP" 
##
##shps = os.listdir(shps_dir)
##shps_H = []
##for i in shps:
##    if '_H_poly.shp' in i:
##        shps_H.append(shps_dir+"\\"+i)
##
##arcpy.AddMessage('Start merging...')
###merge_name = city + "_MERGE.shp"
###merge_result = os.path.join(inWorkspace,merge_name)
merge_result = inWorkspace + "\\" + city + "_MERGE.shp"
###print merge_result
##arcpy.Merge_management(shps_H, merge_result)
##arcpy.AddMessage('Merging succeed!')

#按PID融合
arcpy.AddMessage('Start dissolving...')
dissolve_result = inWorkspace + "\\" + city + "_DISSOLVE.shp"
arcpy.Dissolve_management(merge_result, dissolve_result, ["PID", "FTYPE"])
arcpy.AddMessage('Dissolving succeed!')

#与Tile面交集取反
Outline = ""
arcpy.AddMessage('Start symdiffing...')
for j in os.listdir(inWorkspace):
    #城市分tile匹配，如Suzhou_19Q3_Submit_Grid_M_01.shp
    if ("Submit_Grid_M" in j) and (".shp" in j) and (j.count(".")==1):
        Outline = j
inFeatures = inWorkspace + "\\" + Outline
updateFeatures = dissolve_result
outFeatureClass = inWorkspace + "\\" + city + "_SymDiff.shp"
arcpy.SymDiff_analysis(inFeatures, updateFeatures, outFeatureClass, "ALL", 0.05)
arcpy.AddMessage('Symdiffing succeed!')

#拆分多部件要素
blue = inWorkspace + "\\" + city + "_BLUE.shp"
arcpy.MultipartToSinglepart_management(outFeatureClass, blue)

#漏蓝检查提示消息
feature_count = int(arcpy.GetCount_management(blue).getOutput(0))
if feature_count == 0:
    arcpy.AddMessage("No Blue！Congratulations！".format(feature_count))
elif feature_count == 1:
    arcpy.AddMessage("There is {0} blue gap to confirm！".format(feature_count))
else:
    arcpy.AddMessage("There are {0} blue gaps to confirm！".format(feature_count))

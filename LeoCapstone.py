#Author-Leo
#Description-This is a sketch that aims to give a quick review of the Fusion360
#API

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        #variables
        cirDiamR = 5; #specifies the diameter
        arcDist = cirDiamR / 2; #specifies the arcDistance
        quantity = 3 #specifies the quantity of copies.
     
        #setting app
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design =   app.activeProduct;
        root = adsk.fusion.Component.cast(design.rootComponent);
        
        #setting root sketch and xz plane
        s = root.sketches;
        xz = root.xZConstructionPlane;
        
        #making active sketch and mapping point3D.create() to a variable
        coreP = adsk.core.Point3D.create;
        currentSketch = s.add(xz);
        origin = currentSketch.origin;

        #creating variables that call from currentSketch    
        constraints = currentSketch.geometricConstraints;    
        dimensions = currentSketch.sketchDimensions;
        circles = currentSketch.sketchCurves.sketchCircles;
        arcs = currentSketch.sketchCurves.sketchArcs;
        lines = currentSketch.sketchCurves.sketchLines;
        points = currentSketch.sketchPoints;
        orientations = adsk.fusion.DimensionOrientations;
        
        #creating a center SKETCH point.
        centerPoint = points.add(coreP(0,0,0));
        centerPoint.isFixed = True;
        
        #creating construction lines for x and y axis and constrains to the plane
        lineX = lines.addByTwoPoints(coreP(-cirDiamR,0,0), coreP(cirDiamR,0,0));
        lineY = lines.addByTwoPoints(coreP(0,-cirDiamR,0), coreP(0,cirDiamR,0));
        lineX.isConstruction = True;
        lineY.isConstruction = True;
        constraints.addPerpendicular(lineX, lineY);
        constraints.addCoincident(centerPoint,lineX);
        constraints.addCoincident(centerPoint,lineY);
        constraints.addHorizontal(lineX);
        dimensions.addDistanceDimension(lineX.startSketchPoint, lineX.endSketchPoint,orientations.HorizontalDimensionOrientation, coreP(3,3,0));
        dimensions.addDistanceDimension(lineY.startSketchPoint, lineY.endSketchPoint, orientations.VerticalDimensionOrientation, coreP(3, 4, 0));
        
        #creating initial circle
        innerCircle = circles.addByCenterRadius(centerPoint, cirDiamR);
        dimensions.addRadialDimension(innerCircle,coreP(3,5,0));
        constraints.addCoincident(lineY.endSketchPoint,innerCircle);
        constraints.addCoincident(lineX.endSketchPoint, innerCircle);
        
        #creating initial arc
        arc1 = arcs.addByThreePoints(centerPoint, coreP(-arcDist, arcDist, 0), coreP(0,cirDiamR,0));
        constraints.addCoincident(arc1.startSketchPoint, innerCircle);          
        constraints.addTangent(innerCircle, arc1);
       
  
        #disclosure:
        #       Fusion360 supports circular pattern feature with 3d models but not for sketches.
        #
        #       A work around would be to create a collecion of objects in which you would store what you desire to rotate
        #       You will then proceed to transform the 'normal' sketch throughout the plane you want to rotate it around.
        #       You will need to make a 3d Matrix from which you will need to set your sketch rotation.
        #       You can do this with a simple for loop and a stepping variable where in you'll be copying 
        #       your entities collection accross the rotated matrix.
        #
        #       Downside to this is that the copies will not inherit or create new constraints and therefore you should
        #       think of another work around if you are solely working with the API instead of the GUI.
       
       
        #adding entities to use a quasi-sketch circularPattern feature.
        ent = adsk.core.ObjectCollection.create();
        ent.add(arc1);
        
        normal = currentSketch.xDirection.crossProduct(currentSketch.yDirection);
        normal.transformBy(currentSketch.transform);
        origin.transformBy(currentSketch.transform);
        rotationMatrix = adsk.core.Matrix3D.create();
        step = 2 * math.pi / quantity
        
        for i in range(1, int(quantity)):
            rotationMatrix.setToRotation(step * i, normal, origin)
            currentSketch.copy(ent, rotationMatrix);

    except:
        if ui:
            ui.messageBox('Failed but Rimma fails worse:\n{}'.format(traceback.format_exc()))



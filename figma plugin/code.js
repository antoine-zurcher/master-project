// This plugin will open a window to prompt the user to enter a number, and
// it will then create that many rectangles on the screen.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var _this = this;
// This file holds the main code for the plugins. It has access to the *document*.
// You can access browser APIs in the <script> tag inside "ui.html" which has a
// full browser environment (see documentation).
//import * as data from 'C:/Users/Antoine/CloudStation/EPFL/Master 4/Master project/Dataset/VINS Dataset/JSON/7.json';
//const data = require("C:/Users/Antoine/CloudStation/EPFL/Master 4/Master project/Dataset/VINS Dataset/JSON/7.json");
//console.log(data);
//const url = 'C:/Users/Antoine/CloudStation/EPFL/Master 4/Master project/Dataset/VINS Dataset/JSON/7.json';
/*import data from './example_1.json';
console.log(data);*/
var gray = { r: 0.5, g: 0.5, b: 0.5 };
var lightGray = { r: 0.7, g: 0.7, b: 0.7 };
var black = { r: 0, g: 0, b: 0 };
var white = { r: 1, g: 1, b: 1 };
var red = { r: 1, g: 0, b: 0 };
var dashArray = [5, 5];
function clone(val) {
    var type = typeof val;
    if (val === null) {
        return null;
    }
    else if (type === 'undefined' || type === 'number' ||
        type === 'string' || type === 'boolean') {
        return val;
    }
    else if (type === 'object') {
        if (val instanceof Array) {
            return val.map(function (x) { return clone(x); });
        }
        else if (val instanceof Uint8Array) {
            return new Uint8Array(val);
        }
        else {
            var o = {};
            for (var key in val) {
                o[key] = clone(val[key]);
            }
            return o;
        }
    }
    throw 'unknown';
}
function insert_text(frame, xmin, ymin, xmax, ymax, char, fontSize, i) {
    var text = figma.createText();
    text.fontSize = fontSize;
    text.fontName = { family: "Roboto", style: "Regular" };
    text.characters = char;
    text.x = xmin;
    text.y = ymin;
    text.resize(xmax - xmin, ymax - ymin);
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills = clone(outline.fills);
    fills[0].opacity = 0;
    outline.fills = fills;
    var stroke = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Text '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([text, outline, text_outline], frame).name = 'Text '.concat(i.toString());
}
function insert_image(frame, xmin, ymin, xmax, ymax, i) {
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(xmax - xmin, ymax - ymin);
    rect.cornerRadius = 5;
    var rectFills = clone(rect.fills);
    rectFills[0].color = lightGray;
    rect.fills = rectFills;
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills = clone(outline.fills);
    fills[0].opacity = 0;
    outline.fills = fills;
    var stroke = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Image '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, outline, text_outline], frame).name = 'Image '.concat(i.toString());
}
function insert_icon(frame, xmin, ymin, xmax, ymax, image, i) {
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(xmax - xmin, ymax - ymin);
    var fill = {
        type: "IMAGE",
        scaleMode: "FIT",
        imageHash: image.hash,
    };
    rect.fills = [fill];
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills = clone(outline.fills);
    fills[0].opacity = 0;
    outline.fills = fills;
    var stroke = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Icon '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, outline, text_outline], frame).name = 'Icon '.concat(i.toString());
}
function insert_button(frame, xmin, ymin, xmax, ymax, centerx, centery, char, fontSize, i) {
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(xmax - xmin, ymax - ymin);
    rect.cornerRadius = 5;
    var rectFills = clone(rect.fills);
    rectFills[0].color = gray;
    rect.fills = rectFills;
    var stroke = {
        type: "SOLID",
        color: black
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    var text = figma.createText();
    text.fontSize = fontSize;
    text.fontName = { family: "Roboto", style: "Regular" };
    text.characters = char;
    var textFills = clone(text.fills);
    textFills[0].color = white;
    text.fills = textFills;
    var width = text.width;
    var height = text.height;
    text.x = centerx - width / 2;
    text.y = centery - height / 2;
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills = clone(outline.fills);
    fills[0].opacity = 0;
    outline.fills = fills;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Button '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills_outline = clone(text_outline.fills);
    textFills_outline[0].color = red;
    text_outline.fills = textFills_outline;
    text_outline.name = "outline";
    figma.group([rect, text, outline, text_outline], frame).name = 'Button '.concat(i.toString());
}
function insert_checkedtext(frame, xmin, ymin, xmax, ymax, centerx, centery, char, fontSize, i) {
    var widthComp = xmax - xmin;
    var heightComp = ymax - ymin;
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(heightComp, heightComp);
    rect.cornerRadius = 5;
    var fills = clone(rect.fills);
    fills[0].opacity = 0;
    rect.fills = fills;
    var stroke = {
        type: "SOLID",
        color: gray
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    var text = figma.createText();
    text.fontSize = fontSize;
    text.fontName = { family: "Roboto", style: "Regular" };
    text.characters = char;
    var width = text.width;
    var height = text.height;
    text.x = xmin + 20 + heightComp;
    text.y = centery - height / 2;
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills_outline = clone(outline.fills);
    fills_outline[0].opacity = 0;
    outline.fills = fills_outline;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Check field '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, text, outline, text_outline], frame).name = 'Check field '.concat(i.toString());
}
function insert_edittext(frame, xmin, ymin, xmax, ymax, centerx, centery, char, fontSize, json_data, i) {
    var widthComp = xmax - xmin;
    var heightComp = ymax - ymin;
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(xmax - xmin, ymax - ymin);
    rect.cornerRadius = 5;
    var fills = clone(rect.fills);
    fills[0].opacity = 0;
    rect.fills = fills;
    var stroke = {
        type: "SOLID",
        color: gray
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    var pos_x = xmin + 20;
    var line_x = xmin + 20;
    var nbComponents = Object.keys(json_data).length;
    for (var i_1 = 0; i_1 < nbComponents; i_1++) {
        if (json_data[i_1.toString()].type === "Icon") {
            var icon = json_data[i_1.toString()];
            if ((xmin < icon.center_x && icon.center_x < xmax - widthComp / 2) && (ymin < icon.center_y && icon.center_y < ymax)) {
                pos_x = icon.xmax + 20;
                line_x = icon.xmax + 20;
            }
        }
    }
    var line = figma.createLine();
    line.x = line_x;
    line.y = ymin + 0.8 * heightComp;
    line.rotation = 0;
    line.resize(xmax - 20 - line_x, 0);
    var text = figma.createText();
    text.fontSize = fontSize;
    text.fontName = { family: "Roboto", style: "Regular" };
    text.characters = char;
    var width = text.width;
    var height = text.height;
    text.x = pos_x;
    text.y = centery - height / 2;
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills_outline = clone(outline.fills);
    fills_outline[0].opacity = 0;
    outline.fills = fills_outline;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Input field '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, text, line, outline, text_outline], frame).name = 'Input field '.concat(i.toString());
}
function insert_frame_box(frame, xmin, ymin, xmax, ymax, i) {
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(xmax - xmin, ymax - ymin);
    rect.cornerRadius = 5;
    var fills = clone(rect.fills);
    fills[0].opacity = 0;
    rect.fills = fills;
    var stroke = {
        type: "SOLID",
        color: gray
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills_outline = clone(outline.fills);
    fills_outline[0].opacity = 0;
    outline.fills = fills_outline;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Frame '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, outline, text_outline], frame).name = 'Frame '.concat(i.toString());
}
function insert_page_indicator(frame, xmin, ymin, xmax, ymax, i) {
    var width = xmax - xmin;
    var height = ymax - ymin;
    var center_x = xmin + width / 2;
    var center_y = ymin + height / 2;
    var radius = Math.min(width, height) / 2;
    var outline = figma.createRectangle();
    outline.x = center_x - 4 * radius - 3;
    outline.y = ymin - 3;
    outline.resize(8 * radius + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills_outline = clone(outline.fills);
    fills_outline[0].opacity = 0;
    outline.fills = fills_outline;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Page indicator '.concat(i.toString());
    text_outline.x = center_x - 4 * radius;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    if (width < height) {
        var x = center_x - radius;
        var y1 = center_y - 4 * radius;
        var y2 = center_y - radius;
        var y3 = center_y + 2 * radius;
        var circle1 = figma.createEllipse();
        var circle2 = figma.createEllipse();
        var circle3 = figma.createEllipse();
        circle1.x = x;
        circle2.x = x;
        circle3.x = x;
        circle1.y = y1;
        circle2.y = y2;
        circle3.y = y3;
        circle1.resize(2 * radius, 2 * radius);
        circle2.resize(2 * radius, 2 * radius);
        circle3.resize(2 * radius, 2 * radius);
        var fills = clone(circle1.fills);
        fills[0].opacity = 0;
        var stroke = {
            type: "SOLID",
            color: gray
        };
        circle1.fills = fills;
        circle1.strokes = [stroke];
        circle1.strokeWeight = 5;
        circle1.strokeAlign = "CENTER";
        circle2.fills = fills;
        circle2.strokes = [stroke];
        circle2.strokeWeight = 5;
        circle2.strokeAlign = "CENTER";
        circle3.fills = fills;
        circle3.strokes = [stroke];
        circle3.strokeWeight = 5;
        circle3.strokeAlign = "CENTER";
        figma.group([circle1, circle2, circle3, outline, text_outline], frame).name = 'Page indicator '.concat(i.toString());
    }
    else {
        var x1 = center_x - 4 * radius;
        var x2 = center_x - radius;
        var x3 = center_x + 2 * radius;
        var y = center_y - radius;
        var circle1 = figma.createEllipse();
        var circle2 = figma.createEllipse();
        var circle3 = figma.createEllipse();
        circle1.x = x1;
        circle2.x = x2;
        circle3.x = x3;
        circle1.y = y;
        circle2.y = y;
        circle3.y = y;
        circle1.resize(2 * radius, 2 * radius);
        circle2.resize(2 * radius, 2 * radius);
        circle3.resize(2 * radius, 2 * radius);
        var fills = clone(circle1.fills);
        fills[0].opacity = 0;
        var stroke = {
            type: "SOLID",
            color: gray
        };
        circle1.fills = fills;
        circle1.strokes = [stroke];
        circle1.strokeWeight = 5;
        circle1.strokeAlign = "CENTER";
        circle2.fills = fills;
        circle2.strokes = [stroke];
        circle2.strokeWeight = 5;
        circle2.strokeAlign = "CENTER";
        circle3.fills = fills;
        circle3.strokes = [stroke];
        circle3.strokeWeight = 5;
        circle3.strokeAlign = "CENTER";
        figma.group([circle1, circle2, circle3, outline, text_outline], frame).name = 'Page indicator '.concat(i.toString());
    }
}
function insert_switch(frame, xmin, ymin, xmax, ymax, i) {
    var height = ymax - ymin;
    var radius = height / 2;
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin + 0.25 * height;
    rect.resize(xmax - xmin, 0.5 * height);
    rect.cornerRadius = 0.25 * height;
    var fills = clone(rect.fills);
    fills[0].opacity = 0;
    rect.fills = fills;
    var stroke = {
        type: "SOLID",
        color: gray
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    var circle = figma.createEllipse();
    circle.x = xmin;
    circle.y = ymin;
    circle.resize(2 * radius, 2 * radius);
    var fills_circle = clone(circle.fills);
    fills_circle[0].opacity = 1;
    fills_circle[0].color = white;
    circle.fills = fills_circle;
    var stroke_circle = {
        type: "SOLID",
        color: gray
    };
    circle.strokes = [stroke_circle];
    circle.strokeWeight = 5;
    circle.strokeAlign = "CENTER";
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills_outline = clone(outline.fills);
    fills_outline[0].opacity = 0;
    outline.fills = fills_outline;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Switch 1';
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, circle, outline, text_outline], frame).name = 'Switch '.concat(i.toString());
}
function insert_checkbox(frame, xmin, ymin, xmax, ymax, i) {
    var width = xmax - xmin;
    var height = ymax - ymin;
    var side = Math.min(width, height);
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(side, side);
    rect.cornerRadius = 5;
    var fills = clone(rect.fills);
    fills[0].opacity = 0;
    rect.fills = fills;
    var stroke = {
        type: "SOLID",
        color: gray
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    var outline = figma.createRectangle();
    outline.x = xmin - 3;
    outline.y = ymin - 3;
    outline.resize(xmax - xmin + 6, ymax - ymin + 6);
    outline.cornerRadius = 5;
    var fills_outline = clone(outline.fills);
    fills_outline[0].opacity = 0;
    outline.fills = fills_outline;
    var stroke_outline = {
        type: "SOLID",
        color: red
    };
    outline.strokes = [stroke_outline];
    outline.dashPattern = dashArray;
    outline.strokeWeight = 2;
    outline.strokeAlign = "CENTER";
    outline.name = "outline";
    var text_outline = figma.createText();
    text_outline.fontSize = 20;
    text_outline.fontName = { family: "Roboto", style: "Regular" };
    text_outline.characters = 'Checkbox '.concat(i.toString());
    text_outline.x = xmin;
    text_outline.y = ymin - 30;
    var textFills = clone(text_outline.fills);
    textFills[0].color = red;
    text_outline.fills = textFills;
    text_outline.name = "outline";
    figma.group([rect, outline, text_outline], frame).name = 'Checkbox '.concat(i.toString());
}
function insert_multitab(frame, xmin, ymin, xmax, ymax, nb_textbox, i) {
    var rect = figma.createRectangle();
    rect.x = xmin;
    rect.y = ymin;
    rect.resize(xmax - xmin, ymax - ymin);
    rect.cornerRadius = 5;
    var fills = clone(rect.fills);
    fills[0].opacity = 0;
    rect.fills = fills;
    var stroke = {
        type: "SOLID",
        color: gray
    };
    rect.strokes = [stroke];
    rect.strokeWeight = 5;
    rect.strokeAlign = "CENTER";
    frame.appendChild(rect);
    var line = figma.createLine();
    line.x = xmin;
    line.y = ymax - 5;
    line.rotation = 0;
    line.resize(Math.round((xmax - xmin) / nb_textbox), 0);
    var stroke_line = {
        type: "SOLID",
        color: gray
    };
    line.strokes = [stroke_line];
    line.strokeWeight = 10;
    line.strokeAlign = "CENTER";
    frame.appendChild(line);
}
function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function strToUtf8Bytes(str) {
    var utf8 = [];
    for (var ii = 0; ii < str.length; ii++) {
        var charCode = str.charCodeAt(ii);
        if (charCode < 0x80)
            utf8.push(charCode);
        else if (charCode < 0x800) {
            utf8.push(0xc0 | (charCode >> 6), 0x80 | (charCode & 0x3f));
        }
        else if (charCode < 0xd800 || charCode >= 0xe000) {
            utf8.push(0xe0 | (charCode >> 12), 0x80 | ((charCode >> 6) & 0x3f), 0x80 | (charCode & 0x3f));
        }
        else {
            ii++;
            // Surrogate pair:
            // UTF-16 encodes 0x10000-0x10FFFF by subtracting 0x10000 and
            // splitting the 20 bits of 0x0-0xFFFFF into two halves
            charCode = 0x10000 + (((charCode & 0x3ff) << 10) | (str.charCodeAt(ii) & 0x3ff));
            utf8.push(0xf0 | (charCode >> 18), 0x80 | ((charCode >> 12) & 0x3f), 0x80 | ((charCode >> 6) & 0x3f), 0x80 | (charCode & 0x3f));
        }
    }
    return utf8;
}
function base64ToByteArray(base64String) {
    try {
        var sliceSize = 1024;
        var byteCharacters = atob(base64String);
        var bytesLength = byteCharacters.length;
        var slicesCount = Math.ceil(bytesLength / sliceSize);
        var byteArrays = new Array(slicesCount);
        for (var sliceIndex = 0; sliceIndex < slicesCount; ++sliceIndex) {
            var begin = sliceIndex * sliceSize;
            var end = Math.min(begin + sliceSize, bytesLength);
            var bytes = new Array(end - begin);
            for (var offset = begin, i = 0; offset < end; ++i, ++offset) {
                bytes[i] = byteCharacters[offset].charCodeAt(0);
            }
            byteArrays[sliceIndex] = new Uint8Array(bytes);
        }
        return byteArrays;
    }
    catch (e) {
        console.log("Couldn't convert to byte array: " + e);
        return undefined;
    }
}
var Base64Binary = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    /* will return a  Uint8Array type */
    decodeArrayBuffer: function (input) {
        var bytes = (input.length / 4) * 3;
        var ab = new ArrayBuffer(bytes);
        this.decode(input, ab);
        return ab;
    },
    removePaddingChars: function (input) {
        var lkey = this._keyStr.indexOf(input.charAt(input.length - 1));
        if (lkey == 64) {
            return input.substring(0, input.length - 1);
        }
        return input;
    },
    decode: function (input, arrayBuffer) {
        //get last chars to see if are valid
        input = this.removePaddingChars(input);
        input = this.removePaddingChars(input);
        var bytes = (input.length / 4) * 3;
        var uarray;
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        var j = 0;
        if (arrayBuffer)
            uarray = new Uint8Array(arrayBuffer);
        else
            uarray = new Uint8Array(bytes);
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        for (i = 0; i < bytes; i += 3) {
            //get the 3 octects in 4 ascii chars
            enc1 = this._keyStr.indexOf(input.charAt(j++));
            enc2 = this._keyStr.indexOf(input.charAt(j++));
            enc3 = this._keyStr.indexOf(input.charAt(j++));
            enc4 = this._keyStr.indexOf(input.charAt(j++));
            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;
            uarray[i] = chr1;
            if (enc3 != 64)
                uarray[i + 1] = chr2;
            if (enc4 != 64)
                uarray[i + 2] = chr3;
        }
        return uarray;
    }
};
function bytesArrToBase64(arr) {
    var abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"; // base64 alphabet
    var bin = function (n) { return n.toString(2).padStart(8, 0); }; // convert num to 8-bit binary string
    var l = arr.length;
    var result = '';
    var _loop_1 = function (i) {
        var c1 = i * 3 + 1 >= l; // case when "=" is on end
        var c2 = i * 3 + 2 >= l; // case when "=" is on end
        var chunk = bin(arr[3 * i]) + bin(c1 ? 0 : arr[3 * i + 1]) + bin(c2 ? 0 : arr[3 * i + 2]);
        var r = chunk.match(/.{1,6}/g).map(function (x, j) { return j == 3 && c2 ? '=' : (j == 2 && c1 ? '=' : abc[+('0b' + x)]); });
        result += r.join('');
    };
    for (var i = 0; i <= (l - 1) / 3; i++) {
        _loop_1(i);
    }
    return result;
}
function invertImages(node) {
    return __awaiter(this, void 0, void 0, function () {
        var newFills, _i, _a, paint, image, bytes, b64;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    newFills = [];
                    _i = 0, _a = node.fills;
                    _b.label = 1;
                case 1:
                    if (!(_i < _a.length)) return [3 /*break*/, 4];
                    paint = _a[_i];
                    if (!(paint.type === 'IMAGE')) return [3 /*break*/, 3];
                    image = figma.getImageByHash(paint.imageHash);
                    return [4 /*yield*/, image.getBytesAsync()];
                case 2:
                    bytes = _b.sent();
                    b64 = bytesArrToBase64(bytes);
                    console.log(bytes);
                    console.log(b64);
                    _b.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    });
}
// This shows the HTML page in "ui.html".
figma.showUI(__html__);
// Calls to "parent.postMessage" from within the HTML page will trigger this
// callback. The callback will be passed the "pluginMessage" property of the
// posted message.
figma.ui.onmessage = function (msg) { return __awaiter(_this, void 0, void 0, function () {
    var json_data, nbComponents, frameNode, frame, i_text, i_image, i_icon, i_button, i_edittext, i_switch, i_checkview, i_checkbox, i_tab, i_frame, i_page, i, base64, buffer, uint8Buffer, image, base64, buffer, uint8Buffer, image, selected, frameNode, frameNode, frame, base64, buffer, uint8Buffer, image, rect, fill, pageNodeGod, frameNodeGod, clonedGod, pageNodeUser, frameNodeUser, clonedUser, pageNodeExport, frameNodeExport, outlineNodes;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                if (!(msg.type === 'send-data')) return [3 /*break*/, 2];
                json_data = msg.json_data;
                nbComponents = Object.keys(msg.json_data).length;
                console.log(json_data);
                frameNode = figma.currentPage.findOne(function (n) { return n.type === "FRAME"; });
                if (frameNode) {
                    frameNode.remove();
                }
                frame = figma.createFrame();
                frame.x = 0;
                frame.y = 0;
                frame.resize(1080, 1800);
                return [4 /*yield*/, figma.loadFontAsync({ family: "Roboto", style: "Regular" })];
            case 1:
                _a.sent();
                i_text = 0;
                i_image = 0;
                i_icon = 0;
                i_button = 0;
                i_edittext = 0;
                i_switch = 0;
                i_checkview = 0;
                i_checkbox = 0;
                i_tab = 0;
                i_frame = 0;
                i_page = 0;
                for (i = 0; i < nbComponents; i++) {
                    if (json_data[i.toString()].type === "Text") {
                        i_text++;
                        if (json_data[i.toString()].value) {
                            insert_text(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, capitalize(json_data[i.toString()].value), json_data[i.toString()].font_size - 5, i_text);
                        }
                    }
                    else if (json_data[i.toString()].type === "Image") {
                        if (json_data[i.toString()].value) {
                            i_icon++;
                            base64 = json_data[i.toString()].value.slice(22);
                            buffer = Base64Binary.decodeArrayBuffer(base64);
                            uint8Buffer = new Uint8Array(buffer);
                            image = figma.createImage(Uint8Array.from(uint8Buffer));
                            insert_icon(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, image, i_icon);
                        }
                        else {
                            i_image++;
                            insert_image(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, i_image);
                        }
                    }
                    else if (json_data[i.toString()].type === "Icon") {
                        i_icon++;
                        base64 = json_data[i.toString()].value.slice(22);
                        buffer = Base64Binary.decodeArrayBuffer(base64);
                        uint8Buffer = new Uint8Array(buffer);
                        image = figma.createImage(Uint8Array.from(uint8Buffer));
                        insert_icon(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, image, i_icon);
                    }
                    else if (json_data[i.toString()].type === "TextButton") {
                        i_button++;
                        insert_button(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, json_data[i.toString()].center_x, json_data[i.toString()].center_y, capitalize(json_data[i.toString()].value), json_data[i.toString()].font_size - 5, i_button);
                    }
                    else if (json_data[i.toString()].type === "EditText") {
                        if (json_data[i.toString()].value) {
                            i_edittext++;
                            insert_edittext(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, json_data[i.toString()].center_x, json_data[i.toString()].center_y, capitalize(json_data[i.toString()].value), json_data[i.toString()].font_size - 5, json_data, i_edittext);
                        }
                    }
                    else if (json_data[i.toString()].type === "CheckedTextView") {
                        if (json_data[i.toString()].value) {
                            i_checkview++;
                            insert_checkedtext(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, json_data[i.toString()].center_x, json_data[i.toString()].center_y, capitalize(json_data[i.toString()].value), json_data[i.toString()].font_size - 5, i_checkview);
                        }
                    }
                    else if (json_data[i.toString()].type === "Drawer" ||
                        json_data[i.toString()].type === "Bottom_Navigation" ||
                        json_data[i.toString()].type === "Modal" ||
                        json_data[i.toString()].type === "Card" ||
                        json_data[i.toString()].type === "Toolbar") {
                        i_frame++;
                        insert_frame_box(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, i_frame);
                    }
                    else if (json_data[i.toString()].type === "PageIndicator") {
                        i_page++;
                        insert_page_indicator(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, i_page);
                    }
                    else if (json_data[i.toString()].type === "Switch") {
                        i_switch++;
                        insert_switch(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, i_switch);
                    }
                    else if (json_data[i.toString()].type === "CheckBox" ||
                        json_data[i.toString()].type === "Checkbox") {
                        i_checkbox++;
                        insert_checkbox(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, i_checkbox);
                    }
                    else if (json_data[i.toString()].type === "Multi_Tab") {
                        i_tab++;
                        insert_multitab(frame, json_data[i.toString()].xmin, json_data[i.toString()].ymin, json_data[i.toString()].xmax, json_data[i.toString()].ymax, json_data[i.toString()].value, i_tab);
                    }
                }
                return [3 /*break*/, 8];
            case 2:
                if (!(msg.type === "send-image")) return [3 /*break*/, 3];
                console.log(msg.img_src);
                return [3 /*break*/, 8];
            case 3:
                if (!(msg.type === "check-image")) return [3 /*break*/, 4];
                selected = figma.currentPage.selection[0];
                invertImages(selected);
                return [3 /*break*/, 8];
            case 4:
                if (!(msg.type === "clear")) return [3 /*break*/, 5];
                frameNode = figma.currentPage.findOne(function (n) { return n.type === "FRAME"; });
                if (frameNode) {
                    frameNode.remove();
                }
                return [3 /*break*/, 8];
            case 5:
                if (!(msg.type === "loading")) return [3 /*break*/, 7];
                frameNode = figma.currentPage.findOne(function (n) { return n.type === "FRAME"; });
                if (frameNode) {
                    frameNode.remove();
                }
                frame = figma.createFrame();
                frame.x = 0;
                frame.y = 0;
                frame.resize(1080, 1800);
                return [4 /*yield*/, figma.loadFontAsync({ family: "Roboto", style: "Regular" })];
            case 6:
                _a.sent();
                base64 = 'iVBORw0KGgoAAAANSUhEUgAABDgAAAcICAIAAABW4OboAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAABAAAAAQBPJcTWAABSMUlEQVR42u3de5xk10HY+XNu9fS7p2d6XhppRtLoMRpJo4eRLdnGGGMEkgEHEAKMkWIgWRuyGxIg+zH7SUI2m8d++JCPEy+BxFlYG2KC4WOMjdeJDawJwVh+CCxpLCFp9BxpNI/u6df0+3HP/nGrq29XVfe8untmWt/vH3ZPd3VV3Vul7vPrc8+9MaUUAAAALiWZXQAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKjYBQAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUACiklW/d63o0b+w0AsJ6iH6kArDzyjjHaDwCsMzMqAJdxQqzDozStFH/kAkCoAHDJJZA5FgCECgDL1sIazWyUO8TkybnWXXmP2XsA5//LyM9QgFUcquZ5Pj8/v0Ydki2ojYBrt1mHKY48z+fm5opHXIuFK62trWv0oqzP/I/FPABCBeBSTJTPfe5zf/7nfz4zM7PqP1fLbZBl2e7du9/xjnfcc8896zPsTinNzc196EMf6u/vn5mZWbtBeXt7+zvf+c77779/tR7ilVde+djHPrZu74G77777vvvu898CwGppsQsALtzJkyf/4i/+4tFHH12Hx3r22Wd37979pje9KcuyNforfvluY4xHjx794he/WKuUtZNl2Xd/93cXU0arsl1/9md/tm5/j7v77rv9hwCwmr8U7AKACzc6Onr06NH1eazJycmxsbHZ2dmwZkd81d3tyZMn16FSigfK83x1i8ubE0CoALx+5Xk+Ojq6ng+3nkPw1Y2HFXR3d3svASBUAFbTepZDsWRl3bZotU4PcEYWowMgVAAuvz5Z58ctn1JsPbvo4u5YAIQKwEZwsSYB1udxy0vq13OLnOoXAKECcJ78yX/tdun6zOEAIFQANqDan/wNqVd9lwbrVQCEil0AsIrD641qfdaoSD4AhAoAl1aMxRjNogAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFTsAgAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAnA5SSnZCQAgVAAAAKECAAAgVAAucXXHemWZn6gAIFQALrYY4wrdAgAIFYCLoK5M6roFABAqABeBGZW1aD+9B4BQAVg1LS0tfX199sOq5J/kA0CoAKyO1tbWHTt2hI01r7L+25JlWYzRpAoAQgVgdWzatKmzszNsrJUqtW1Zt41qbW31XgJAqACsml27dnV0dKzbw83MzJTPhrzWUx/z8/Pr1nveSwAIFYBVUERCjLGrq2vdHnRiYqIcJ2sx41Hcf/G/6xYqbW1tjvsCQKgArKbi0K/1MTY2tnbxUEuv2v+u22IVh34BIFQAVkdtKL/OoZLn+ZpuUdnIyMj6bFdPT493FABCBWA1B/c9PT0ppfWZfJicnFy7UGk0NTW1Pg/U3d3tvQSAUAG4UOUs6e3tXbdT687MzKznZq7bw63nOh8AhArAhlXOks7OznVbCD40NDQ3N7dum3ny5Mn1eaC2trawsa5FA4BQAbjIOjo61m2EPTExcfr06fV5rDzPjx8/vp6h4sRfAAgVgFXT3t6+bo8VY3zttdfW57FeeOGFdZ5RAQChArAKiomU9Rxkp5ReeOGF9XmsV199dWBgQKgAIFQALjPFoUrd3d2VSmXdHvSpp54aHx9f0/SqPdDExMQ6bFFXV9fWrVu9nQAQKgCrqbOzc9u2bev2cIcOHXr++efXNL2KYnniiSfWZ4v279+/njsQAKEC8LrQ0tJy7bXXrtt6+rGxsa997WtrdOe1rXjppZfWLofqXH/99Vu2bCk/utN/AQgVAC7452mW3XHHHet59Ndf/uVfrtFlH2szKp/73OfW7TzIBw4cKPZe7dGd/gtAqACwCu68886Ojo51e7gjR4586UtfuvD7WW7ior+//4//+I/XbXOuu+46ZQKAUAFYffv27evu7l63h8vz/Dd+4zfGxsbOMjyW05gHxT188pOfXJ+rtcQYOzo6du/efYEbAoBQAaCJjo6OPXv2NDbA2k0UvPLKK7/5m79ZdwBYjDGldB6j/Nq3xBg/+9nPfuYznyk+s0bBUF6yv3fv3tbW1jMWFABCBYDzce2115bH/Ws60C98+tOf/tSnPlX3KDHG8xjlF4UTQjh06NBv/uZvTk9PF59Z9WBo3C0HDhzIsiyYRQFAqACshb1795bH/WvxEI13+2u/9msf+tCHVmVhfYzxC1/4ws///M+PjIys3VbU3WdbW9vBgwfXdKcBcNlpsQsAzlvjbMM111zT1tY2PT1dG3YXUwS1D1blQRs/+dnPfvbEiRMPPfTQbbfddt5bMTw8/Mu//MuPPPJIbSJljaZTygd9hRB6enruvPNObycAhArA6mgcxF955ZUHDhx4/PHH6+JkjY5oKg/6v/a1rz333HPf9V3f9eM//uM9PT3ntBXj4+OPPvroxz/+8eeee662rqa481VMrHK8le9/8+bNO3bsWLkAARAqAJx/M2zbtu26664rQmVNl1vURvnlzwwODv7e7/3en/zJn7z73e++9957r7rqqjMO90dGRr7+9a9/8pOffPbZZ+uecPG9a7EV5XMMpJR6e3uXK0DFAiBUAFiFwXelUnnjG9/4qU99qjy8XvVJidBsMqc27h8cHPyt3/qt3/md3+ns7Lz11lv379/f09OzefPmrq6u1tbW8fHxkZGR4eHh/v7+p59++tVXX52amrooPVB70O/4ju84+80EQKgAcD5uueWWvr6+oaGh8oh8nXsphDA3Nzc6OvrII4888sgjtaeRZVnTJ7OePVDrk2JGaN++fffcc4+3DQB1nPULYJVt2bLl/vvvX/9EOWNvrMXEzgU+yZTSO9/5zp07dzorMQBCBWDNPfjggx0dHWHdj1wqD/cv2aF/eWlNa2vru9/97uAQLwCECsA66Ovr+5Zv+ZZQuubj+gTAcv9c4TnU3WwdgqG8T771W7918+bN3jAACBWAdfK93/u9HR0d53eF+PMOgLNsmHKT1F3Pfj3nYVpbW3/4h384uBo9AEIFYN3ccccdN9988yX79C6F9So33HBDsYsc9wWAUAFYJ52dnd///d9/0Z/GCjVS96X175Z7773X+wQAoQKw3u6+++6dO3eu0ADr0AYrTFassKZl1Rupdghc7ZP79+//tm/7Nm8SAIQKwDqpjcXb29vLp7SqlUDjBxtS3TL9YrfUPvnt3/7t27dv924BQKgArN8AvdYqDzzwwO7du+sCZj1PBXZp2rJly7ve9S5r6AEQKgDr3SrFB52dnQ899NCmTZuWu8HrTUqppaXlF37hF7Zu3WoNPQBCBeCiuf/++9/xjne8bje/btokxviud73rbW9728o3AwChArC2A/Qsy37qp35q7969r8OheYwxy5b8orn11lsffvjhprf0ngFAqACsxxi99vEVV1zxi7/4i5VK5fU2NK9bjdPS0vLwww/v2LHj9ZNqAAgVgEtujF7+5y233PLAAw+c8WYbe4e8733vu+eee15XqQaAUAG4tDSOwt/3vve98Y1vbHp1kQ08cK9t1B133PHQQw95YwAgVAAuLV1dXQ8//HBvb2/xz5RSnuflG9Qa5vIqlpWfbXH0186dO3/6p3/aewAAoQJwKbr99tt/8id/snbpw+WG+JfX8WBNLwtT/kyWZQ899NDNN9/sDQCA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BQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCxS4AAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBU7AIAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAIFQAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAKECAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAAAgVAAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAELFLgAAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAAIQKAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAACAUAEAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAABAqAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAAQgUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAECoAAAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAACBUAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAAChAgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAIFQAAACECgAAgFABAACECgAAgFABAACECgAAgFABAACECgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAgFABAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAAAQKgAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAEIFAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAABAqAAAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAAAgVAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAoQIAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAACBUAAAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAhAoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAIBQAQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAECoAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAABCBQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAAAIFQAAQKgAAABcQv5/ob51brFT9HYAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDUtMjBUMTI6MTc6NDYrMDA6MDDImbQLAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTA1LTIwVDEyOjE3OjQ2KzAwOjAwucQMtwAAAABJRU5ErkJggg==';
                buffer = Base64Binary.decodeArrayBuffer(base64);
                uint8Buffer = new Uint8Array(buffer);
                image = figma.createImage(Uint8Array.from(uint8Buffer));
                rect = figma.createRectangle();
                rect.x = 0;
                rect.y = 0;
                rect.resize(1080, 1800);
                fill = {
                    type: "IMAGE",
                    scaleMode: "FIT",
                    imageHash: image.hash,
                };
                rect.fills = [fill];
                frame.appendChild(rect);
                return [3 /*break*/, 8];
            case 7:
                if (msg.type === "sync") {
                    pageNodeGod = figma.root.children.find(function (n) { return n.name === "God"; });
                    frameNodeGod = pageNodeGod.findOne(function (n) { return n.type === "FRAME"; });
                    clonedGod = frameNodeGod.clone();
                    pageNodeUser = figma.root.children.find(function (n) { return n.name === "User"; });
                    frameNodeUser = pageNodeUser.findOne(function (n) { return n.type === "FRAME"; });
                    if (frameNodeUser) {
                        frameNodeUser.remove();
                    }
                    pageNodeUser.appendChild(clonedGod);
                    clonedUser = pageNodeUser.findOne(function (n) { return n.type === "FRAME"; }).clone();
                    pageNodeExport = figma.root.children.find(function (n) { return n.name === "Export"; });
                    frameNodeExport = pageNodeExport.findOne(function (n) { return n.type === "FRAME"; });
                    if (frameNodeExport) {
                        frameNodeExport.remove();
                    }
                    pageNodeExport.appendChild(clonedUser);
                    outlineNodes = pageNodeExport.findAll(function (n) { return n.name === "outline"; });
                    outlineNodes.forEach(function (node) { return node.remove(); });
                }
                _a.label = 8;
            case 8: return [2 /*return*/];
        }
    });
}); };

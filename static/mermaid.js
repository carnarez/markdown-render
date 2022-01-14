// variables from https://github.com/mermaid-js/mermaid/blob/develop/src/themes/theme-base.js

function mermaidInitialize() {
  let style = getComputedStyle(document.body);

  // main

  let darkMode = document.documentElement.className === "light" ? false : true;

  let background = style.getPropertyValue("--background-color");
  let fontFamily = style.getPropertyValue("--font-family");
  let fontSize = style.getPropertyValue("--font-size");

  let textColor = style.getPropertyValue("--font-color");
  let linkColor = style.getPropertyValue("--link-color");

  let primaryColor = style.getPropertyValue("--background-color-alt");
  let primaryBorderColor = primaryColor;
  let primaryTextColor = textColor;

  let secondaryColor = primaryColor;
  let secondaryBorderColor = primaryColor;
  let secondaryTextColor = textColor;

  let tertiaryColor = primaryColor;
  let tertiaryBorderColor = primaryColor;
  let tertiaryTextColor = textColor;

  let noteBkgColor = background;
  let noteTextColor = linkColor;
  let noteBorderColor = linkColor;

  let lineColor = textColor;

  // flowchart

  let mainBkg = primaryColor;

  let nodeBkg = primaryColor;
  let nodeBorder = background;
  let nodeTextColor = textColor;

  let clusterBkg = background;
  let clusterBorder = primaryColor;

  let defaultLinkColor = lineColor;
  let titleColor = textColor;

  let edgeLabelBackground = background;

  // sequence diagram

  let actorBkg = primaryColor;
  let actorBorder = primaryColor;
  let actorLineColor = textColor;
  let actorTextColor = textColor;

  let labelBoxBkgColor = primaryColor;
  let labelBoxBorderColor = primaryColor;
  let labelTextColor = textColor;

  let signalColor = textColor;
  let signalTextColor = textColor;

  let loopTextColor = actorTextColor;

  let activationBkgColor = primaryColor;
  let activationBorderColor = background;

  let sequenceNumberColor = background;

  // gantt chart

  let sectionBkgColor = primaryColor;
  let sectionBkgColor2 = background;
  let altSectionBkgColor = background;

  let gridColor = lineColor;

  let todayLineColor = linkColor;

  let excludeBkgColor = background;

  let taskBorderColor = linkColor;
  let taskBkgColor = primaryColor;

  let activeTaskBorderColor = primaryColor;
  let activeTaskBkgColor = primaryColor;

  let doneTaskBkgColor = background;
  let doneTaskBorderColor = primaryColor;

  let critBkgColor = "red";
  let critBorderColor = "red";

  let taskTextColor = textColor;
  let taskTextOutsideColor = textColor;
  let taskTextLightColor = textColor;
  let taskTextDarkColor = textColor;
  let taskTextClickableColor = linkColor;

  // state diagram

  let labelBackgroundColor = background;

  let stateBkg = primaryColor;
  let stateLabelColor = textColor;
  let altBackground = primaryColor;

  let compositeBackground = primaryColor;
  let compositeBorder = textColor;
  let compositeTitleBackground = primaryColor;

  let innerEndBackground = primaryColor;

  let errorBkgColor = background;
  let errorTextColor = linkColor;

  let transitionColor = lineColor;
  let transitionLabelColor = textColor;

  let specialStateColor = lineColor;

  // class diagram

  let classText = textColor;

  // user journey

  let fillType0 = primaryColor;
  let fillType1 = secondaryColor;
  let fillType2 = primaryColor;
  let fillType3 = secondaryColor;
  let fillType4 = primaryColor;
  let fillType5 = secondaryColor;
  let fillType6 = primaryColor;
  let fillType7 = secondaryColor;

  // requirement diagram

  let requirementBackground = primaryColor;
  let requirementBorderColor = background;
  let requirementBorderSize = "1px";
  let requirementTextColor = textColor;

  let relationColor = lineColor;
  let relationLabelBackground = background;
  let relationLabelColor = textColor;

  // let's make it happen

  mermaid.initialize({
    "theme": "base",
    "themeVariables": {
      "activationBkgColor": activationBkgColor,
      "activationBorderColor": activationBorderColor,
      "activeTaskBkgColor": activeTaskBkgColor,
      "activeTaskBorderColor": activeTaskBorderColor,
      "actorBkg": actorBkg,
      "actorBorder": actorBorder,
      "actorLineColor": actorLineColor,
      "actorTextColor": actorTextColor,
      "altBackground": altBackground,
      "altSectionBkgColor": altSectionBkgColor,
      "background": background,
      "classText": classText,
      "clusterBkg": clusterBkg,
      "clusterBorder": clusterBorder,
      "compositeBackground": compositeBackground,
      "compositeBorder": compositeBorder,
      "compositeTitleBackground": compositeTitleBackground,
      "critBkgColor": critBkgColor,
      "critBorderColor": critBorderColor,
      "darkMode": darkMode,
      "defaultLinkColor": defaultLinkColor,
      "doneTaskBkgColor": doneTaskBkgColor,
      "doneTaskBorderColor": doneTaskBorderColor,
      "edgeLabelBackground": edgeLabelBackground,
      "errorBkgColor": errorBkgColor,
      "errorTextColor": errorTextColor,
      "excludeBkgColor": excludeBkgColor,
      "fillType0": fillType0,
      "fillType1": fillType1,
      "fillType2": fillType2,
      "fillType3": fillType3,
      "fillType4": fillType4,
      "fillType5": fillType5,
      "fillType6": fillType6,
      "fillType7": fillType7,
      "fontFamily": fontFamily,
      "fontSize": fontSize,
      "gridColor": gridColor,
      "innerEndBackground": innerEndBackground,
      "labelBackgroundColor": labelBackgroundColor,
      "labelBoxBkgColor": labelBoxBkgColor,
      "labelBoxBorderColor": labelBoxBorderColor,
      "labelTextColor": labelTextColor,
      "lineColor": lineColor,
      "loopTextColor": loopTextColor,
      "mainBkg": mainBkg,
      "nodeBkg": nodeBkg,
      "nodeBorder": nodeBorder,
      "nodeTextColor": nodeTextColor,
      "noteBkgColor": noteBkgColor,
      "noteBorderColor": noteBorderColor,
      "noteTextColor": noteTextColor,
      "primaryBorderColor": primaryBorderColor,
      "primaryColor": primaryColor,
      "primaryTextColor": primaryTextColor,
      "relationColor": relationColor,
      "relationLabelBackground": relationLabelBackground,
      "relationLabelColor": relationLabelColor,
      "requirementBackground": requirementBackground,
      "requirementBorderColor": requirementBorderColor,
      "requirementBorderSize": requirementBorderSize,
      "requirementTextColor": requirementTextColor,
      "secondaryBorderColor": secondaryBorderColor,
      "secondaryColor": secondaryColor,
      "secondaryTextColor": secondaryTextColor,
      "sectionBkgColor2": sectionBkgColor2,
      "sectionBkgColor": sectionBkgColor,
      "sequenceNumberColor": sequenceNumberColor,
      "signalColor": signalColor,
      "signalTextColor": signalTextColor,
      "specialStateColor": specialStateColor,
      "stateBkg": stateBkg,
      "stateLabelColor": stateLabelColor,
      "taskBkgColor": taskBkgColor,
      "taskBorderColor": taskBorderColor,
      "taskTextClickableColor": taskTextClickableColor,
      "taskTextColor": taskTextColor,
      "taskTextDarkColor": taskTextDarkColor,
      "taskTextLightColor": taskTextLightColor,
      "taskTextOutsideColor": taskTextOutsideColor,
      "tertiaryBorderColor": tertiaryBorderColor,
      "tertiaryColor": tertiaryColor,
      "tertiaryTextColor": tertiaryTextColor,
      "textColor": textColor,
      "titleColor": titleColor,
      "todayLineColor": todayLineColor,
      "transitionColor": transitionColor,
      "transitionLabelColor": transitionLabelColor,
    }
  });
}

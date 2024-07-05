class Selector{

    static selectImage(data, tr){
        Selector.resetSelection();
        Selector.SELECTED = new Selected(data, tr, true, false, false);
        tr.setAttribute("selected", "");
        Selector.updateButtons("image");
    }

    static selectGif(data, tr){
        Selector.resetSelection();
        Selector.SELECTED = new Selected(data, tr, false, true, false);
        tr.setAttribute("selected", "");
        Selector.updateButtons("gif");
    }

    static selectPlugin(data, tr){
        Selector.resetSelection();
        Selector.SELECTED = new Selected(data, tr, false, false, true);
        tr.setAttribute("selected", "");
        Selector.updateButtons("plugin");
    }

    static resetSelection(){
        if(Selector.SELECTED.getTr() != null){
            Selector.SELECTED.getTr().removeAttribute("selected");
        }
    }

    static updateButtons(selectedType){
        switch(selectedType){
            case "image":
                break
            case "gif":
                break
            case "plugin":
                break
            default:
        }
    }

    static getSelected(){
        return Selector.SELECTED
    }

}

class Selected{
    constructor(data, tr, isImage, isGif, isPlugin){
        this.data = data
        this.isImage = isImage
        this.isGif = isGif
        this.isPlugin = isPlugin
        this.tr = tr
    }

    getTr(){
        return this.tr
    }

    getData(){
        return this.data;
    }

    getName(){
        return this.data.name;
    }

    getSettings(){
        return this.data.settings;
    }

    get(key){
        if(key == null)return this.data;
        if("settings" in this.data){
            if(key in this.data.settings)return this.data.settings[key];
        }
        if(key in this.data)return this.data[key];
        return null;
    }

    getType(){
        if(this.isImage)return "image";
        if(this.isGif)return "gif";
        if(this.isPlugin)return "plugin";
        return null;
    }
}

Selector.SELECTED = new Selected(null, null, false, false, false)
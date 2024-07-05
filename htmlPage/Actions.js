class Actions{

    static async clear(){
        return Matrix.clear();
    }

    static async show(type, name){
        if(type == "image"){
            return Matrix.loadImage(name);
        }else if(type == "gif"){
            return Matrix.loadAnimation(name);
        }else if(type == "plugin"){
            return Matrix.loadPlugin(name);
        }
    }

    static async delete(type, name){

        let wantDelete = confirm(`Are you sure you want to delete ${name}?`);
        if(!wantDelete)return;
        if(type == "image"){
            return Matrix.deleteImage(name);
        }else if(type == "gif"){
            return Matrix.deleteGif(name);
        }else if(type == "plugin"){
            return Matrix.deletePlugin(name);
        }
    }

    static async upload(name, data){
        return Matrix.upload(name, data);
    }

    static async edit(type, name, args){
        return Matrix.edit(type, name, args);
    }

}
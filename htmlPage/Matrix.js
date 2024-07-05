class Matrix{

    static async loadImage(name){
        return Matrix.sendRequest({
            action: 'loadImage',
            name: name,
        });
    }

    static async loadAnimation(name){
        return Matrix.sendRequest({
            action: 'loadGif',
            name: name,
        });
    }

    static async loadPlugin(name){
        return Matrix.sendRequest({
            action: 'loadPlugin',
            name: name
        });
    }

    static async clear(){
        return Matrix.sendRequest({
            action: 'clear'
        });
    }

    static async getPlugins(){
        return Matrix.sendRequest({
            action: 'getPlugins'
        });
    }

    static async getImages(){
        return Matrix.sendRequest({
            action: 'getImages'
        });
    }

    static async getGifs(){
        return Matrix.sendRequest({
            action: 'getGifs'
        });
    }

    static async getAllData(){
        return Matrix.sendRequest({
            action: 'getAllData'
        });
    }

    static async setBrightness(value){
        return Matrix.sendRequest({
            action: 'setBrightness',
            brightness: value
        });
    }

    static async getCurrentDisplay(){
        return Matrix.sendRequest({
            action: 'getCurrentDisplay'
        });
    }

    static async upload(name, data, encryption="base64"){
        return Matrix.sendRequest({
            action: 'upload',
            name: name,
            data: data,
            encryption: encryption
        }, 10*60*1000);
    }

    static async deletePlugin(name){
        return Matrix.sendRequest({
            action: 'deletePlugin',
            name: name
        });
    }

    static async deleteImage(name){
        return Matrix.sendRequest({
            action: 'deleteImage',
            name: name
        });
    }

    static async deleteGif(name){
        return Matrix.sendRequest({
            action: 'deleteGif',
            name: name
        });
    }

    static async getPluginConfig(name){
        return Matrix.sendRequest({
            action: 'getPluginConfig',
            name: name
        });
    }

    static async savePluginConfig(name, config){
        return Matrix.sendRequest({
            action: 'savePluginConfig',
            name: name,
            config: config
        });
    }

    static async edit(type, name, data){
        if(type == "image"){
            return Matrix.editImage(name, data);
        }else if(type == "gif"){
            return Matrix.editGif(name, data);
        }else if(type == "plugin"){
            return Matrix.editPlugin(name, data);
        }
    }

    static async editImage(name, data){
        return Matrix.sendRequest({
            action: 'editImage',
            name: name,
            data: data
        });
    }

    static async editGif(name, data){
        return Matrix.sendRequest({
            action: 'editGif',
            name: name,
            data: data
        });
    }

    static async editPlugin(name, data){
        return Matrix.sendRequest({
            action: 'editPlugin',
            name: name,
            data: data
        });
    }

    static sendRequest(data, timeout=10000){
        let requestURL = 'http://localhost:2222/matrix/wrapper.php';

        if(location.protocol == "https:" && location.hostname != "localhost" && location.hostname != "" && location.hostname != "172.0.0.1"){
            requestURL = 'https://led-matrix.frobeen.com/wrapper.php';
        }

        return new Promise((resolve, reject) => {
            $.ajax({
                url: requestURL,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: (response) => {
                    resolve(response);
                },
                error: (err) => {
                    reject(err);
                },
                timeout: timeout,
                cache: false
            });
        });
    }

}
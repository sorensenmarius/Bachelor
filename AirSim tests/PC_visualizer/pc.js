var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 0.1, 1000 );

var geometry = new THREE.SphereGeometry( 0.1, 32, 32 );
var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
var light = new THREE.PointLight( 0xff0000, 1, 100 );
light.position.set( 10, 10, 10 );

scene.add(light)
var list;
var currentLine = 0;


camera.position.z = 5;

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

var p;
var sphere;
function addLidarPoints(scene) {
    fetch('../lidar.txt')
    .then(res => res.text())
    .then(text => {
        list = text.split("\n");
        for(let i = currentLine; i < list.length; i++) {
            p = list[i];
            sphere = new THREE.Mesh(geometry, material);
            point = p.split(" ");
            sphere.position.x = parseFloat(point[0])
            sphere.position.y = parseFloat(point[1])
            sphere.position.z = parseFloat(point[2])
            scene.add(sphere);
            
            
            currentLine += 1;
        }
    })
}

function animate() {
    requestAnimationFrame(animate);
    addLidarPoints(scene);
    renderer.render(scene, camera);
    camera.rotation.y += Math.PI / 180
}

animate()
use ndarray::Array;
use rand::Rng;

fn main() {
    let mut rng = rand::thread_rng();
    let rows = 4;
    let cols = 2;
    let mut array = Array::zeros((rows, cols));
    for mut row in array.genrows_mut() {
        for element in row.iter_mut() {
            *element = rng.gen_range(0.0..10.0)
        }
    }
    println!("Random Array:\n{}", array);
}

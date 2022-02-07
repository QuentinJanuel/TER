mod lf;
mod af;
mod utils;
mod problem;

use af::AF;
use utils::args::Args;

fn main() {
    let args = Args::new();
    if args.has("--problems") {
        problem::all_problems();
    } else if args.has("--formats") {
        println!("[tgf]");
    } else if let Some(problem) = args.get("-p") {
        let param = args.get("-a");
        let problem = (problem, param).into();
        let file = args.get("-f")
            .expect("The file is not specified");
        let tgf = utils::read_file(file);
        let af = AF::from_tgf(&tgf);
        let lf = af.phi(&problem);
        println!("Problem: {}", problem);
        println!("AF:\n{}", af);
        println!("LF:\n{}", lf);
    } else {
        utils::details();
    }
}

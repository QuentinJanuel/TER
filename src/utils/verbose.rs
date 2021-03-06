use std::sync::{Arc, Mutex};
use lazy_static::lazy_static;

pub struct Verbose {
    value: Arc<Mutex<bool>>,
}

impl Verbose {
    fn new() -> Self {
        Self {
            value: Arc::new(Mutex::new(false)),
        }
    }
    pub fn enable(&self) {
        *self.value.lock().unwrap() = true;
    }
    pub fn val(&self) -> bool {
        *self.value.lock().unwrap()
    }
}

lazy_static! {
    pub static ref VERBOSE: Verbose = Verbose::new();
}

#[macro_export]
macro_rules! log {
    ($($arg:tt)*) => ({
        if $crate::utils::verbose::VERBOSE.val() {
            println!($($arg)*);
        }
    })
}

#[macro_export]
macro_rules! benchmark {
    ($name:expr, $code:expr $(,)?) => ({
        log!("{}...", $name);
        let now = std::time::Instant::now();
        let result = $code;
        log!("{} done in {}ms", $name, now.elapsed().as_millis());
        result
    })
}

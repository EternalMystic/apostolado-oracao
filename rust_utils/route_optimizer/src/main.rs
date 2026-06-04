//! Otimizador de rota – vizinho mais próximo (TSP heurístico).
//! Entrada: IDs e coordenadas (lat lon) separados por espaço, uma linha por ponto.
//! Saída: ordem otimizada dos IDs.

use std::env;
use std::f64::consts::PI;
use std::io::{self, BufRead};

#[derive(Clone, Copy)]
struct Point {
    id: i32,
    lat: f64,
    lon: f64,
}

fn dist(a: Point, b: Point) -> f64 {
    let rlat1 = a.lat * PI / 180.0;
    let rlat2 = b.lat * PI / 180.0;
    let dlat = (b.lat - a.lat) * PI / 180.0;
    let dlon = (b.lon - a.lon) * PI / 180.0;
    let h = (dlat / 2.0).sin().powi(2)
        + rlat1.cos() * rlat2.cos() * (dlon / 2.0).sin().powi(2);
    6371.0 * 2.0 * h.sqrt().asin()
}

fn nearest_neighbor(points: &[Point], start: usize) -> Vec<usize> {
    let n = points.len();
    let mut visited = vec![false; n];
    let mut order = Vec::with_capacity(n);
    let mut current = start;
    visited[current] = true;
    order.push(current);

    for _ in 1..n {
        let mut best: Option<usize> = None;
        let mut best_d = f64::MAX;
        for j in 0..n {
            if visited[j] {
                continue;
            }
            let d = dist(points[current], points[j]);
            if d < best_d {
                best_d = d;
                best = Some(j);
            }
        }
        current = best.expect("vizinho");
        visited[current] = true;
        order.push(current);
    }
    order
}

fn main() {
    let stdin = io::stdin();
    let mut points: Vec<Point> = Vec::new();

    for line in stdin.lock().lines() {
        let line = line.expect("linha");
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() < 3 {
            eprintln!("Formato: id lat lon");
            continue;
        }
        let id: i32 = parts[0].parse().expect("id");
        let lat: f64 = parts[1].parse().expect("lat");
        let lon: f64 = parts[2].parse().expect("lon");
        points.push(Point { id, lat, lon });
    }

    if points.is_empty() {
        eprintln!("Uso: route_optimizer < pontos.txt");
        eprintln!("Exemplo:");
        eprintln!("  1 -22.783 -47.296");
        eprintln!("  2 -22.785 -47.298");
        return;
    }

    let start = env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(0)
        .min(points.len().saturating_sub(1));

    let order = nearest_neighbor(&points, start);
    print!("Ordem otimizada:");
    for idx in order {
        print!(" {}", points[idx].id);
    }
    println!();

    let mut total = 0.0;
    for w in order.windows(2) {
        total += dist(points[w[0]], points[w[1]]);
    }
    println!("Distância aproximada: {:.2} km", total);
}

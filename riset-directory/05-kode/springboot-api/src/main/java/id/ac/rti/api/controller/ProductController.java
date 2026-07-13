package id.ac.rti.api.controller;

import id.ac.rti.api.model.Product;
import id.ac.rti.api.repository.ProductRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller CRUD untuk koleksi ikea_products.
 *
 * Endpoints:
 *   GET    /api/products          — ambil semua produk
 *   GET    /api/products/{id}     — ambil produk by MongoDB _id
 *   POST   /api/products          — tambah produk baru
 *   PUT    /api/products/{id}     — update produk by MongoDB _id
 *   DELETE /api/products/{id}     — hapus produk by MongoDB _id
 */
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductRepository repository;

    public ProductController(ProductRepository repository) {
        this.repository = repository;
    }

    // ── READ ALL ──────────────────────────────────────────────────────────────

    @GetMapping
    public List<Product> getAll(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        org.springframework.data.domain.Pageable pageable =
                org.springframework.data.domain.PageRequest.of(page, size);
        return repository.findAll(pageable).getContent();
    }

    // ── READ ONE ──────────────────────────────────────────────────────────────

    @GetMapping("/{id}")
    public ResponseEntity<Product> getById(@PathVariable String id) {
        return repository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // ── CREATE ────────────────────────────────────────────────────────────────

    @PostMapping
    public ResponseEntity<Product> create(@RequestBody Product product) {
        Product saved = repository.save(product);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    // ── UPDATE ────────────────────────────────────────────────────────────────

    @PutMapping("/{id}")
    public ResponseEntity<Product> update(@PathVariable String id,
                                          @RequestBody Product updated) {
        return repository.findById(id)
                .map(existing -> {
                    updated.setId(existing.getId());
                    return ResponseEntity.ok(repository.save(updated));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    // ── DELETE ────────────────────────────────────────────────────────────────

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id) {
        if (!repository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        repository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}

package id.ac.rti.api.repository;

import id.ac.rti.api.model.Product;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends MongoRepository<Product, String> {
    // MongoRepository sudah menyediakan: findAll, findById, save, deleteById, count
}

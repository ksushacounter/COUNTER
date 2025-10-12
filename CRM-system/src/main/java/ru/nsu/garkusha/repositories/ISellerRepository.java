package ru.nsu.garkusha.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import ru.nsu.garkusha.entities.Seller;
import java.util.List;
import java.util.Optional;

public interface ISellerRepository extends JpaRepository<Seller, Long> {

    @Query("SELECT s FROM Seller s WHERE s.deleted = false")
    List<Seller> findAllActive();

    @Query("SELECT s FROM Seller s WHERE s.id = :id AND s.deleted = false")
    Optional<Seller> findActiveById(Long id);

    @Query("SELECT CASE WHEN COUNT(s) > 0 THEN true ELSE false END FROM Seller s WHERE s.id = :id AND s.deleted = false")
    boolean existsActiveById(Long id);
}
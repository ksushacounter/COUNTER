package ru.nsu.garkusha.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.entities.Transaction;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface ITransactionRepository extends JpaRepository<Transaction, Long> {

    @Query("SELECT t FROM Transaction t WHERE t.deleted = false")
    List<Transaction> findAllActive();

    @Query("SELECT t FROM Transaction t WHERE t.id = :id AND t.deleted = false")
    Optional<Transaction> findActiveById(Long id);

    @Query("SELECT t FROM Transaction t WHERE t.seller.id = :sellerId AND t.deleted = false")
    List<Transaction> findActiveBySellerId(Long sellerId);

    @Query("SELECT t FROM Transaction t WHERE t.seller.id = :sellerId AND t.deleted = false ORDER BY t.transactionDate ASC")
    List<Transaction> findActiveBySellerIdOrderByTransactionDateAsc(Long sellerId);

    @Query("SELECT t.seller FROM Transaction t " +
            "WHERE t.transactionDate BETWEEN :start AND :end AND t.deleted = false AND t.seller.deleted = false " +
            "GROUP BY t.seller " +
            "ORDER BY SUM(t.amount) DESC")
    List<Seller> findMostProductiveSellers(LocalDateTime start, LocalDateTime end);

    @Query("SELECT t.seller FROM Transaction t WHERE t.transactionDate BETWEEN :start AND :end AND t.deleted = false AND t.seller.deleted = false GROUP BY t.seller HAVING SUM(t.amount) < :amount")
    List<Seller> findSellersWithTotalAmountLessThan(double amount, LocalDateTime start, LocalDateTime end);
}
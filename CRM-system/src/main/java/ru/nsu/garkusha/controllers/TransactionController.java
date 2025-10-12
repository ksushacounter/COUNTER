package ru.nsu.garkusha.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.nsu.garkusha.dto.Period;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.entities.Transaction;
import ru.nsu.garkusha.services.TransactionService;
import ru.nsu.garkusha.exception.InvalidPeriodException;
import ru.nsu.garkusha.exception.SellerNotFoundException;

import jakarta.validation.Valid;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@Validated
public class TransactionController {

    private final TransactionService transactionService;

    @Autowired
    public TransactionController(TransactionService transactionService) {
        this.transactionService = transactionService;
    }

    @GetMapping
    public List<Transaction> getAllTransactions() {
        return transactionService.transactionsList();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Transaction> getTransactionById(@PathVariable Long id) {
        return transactionService.transactionById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<?> createTransaction(@Valid @RequestBody Transaction transaction) {
        try {
            Transaction created = transactionService.createTransaction(transaction);
            return ResponseEntity.ok(created);
        } catch (SellerNotFoundException e) {
            return ResponseEntity.status(404).body(e.getMessage());
        }
    }

    @GetMapping("/seller/{sellerId}")
    public ResponseEntity<List<Transaction>> getTransactionsBySellerId(@PathVariable Long sellerId) {
        try {
            List<Transaction> transactions = transactionService.allSellerTransactions(sellerId);
            return ResponseEntity.ok(transactions);
        } catch (SellerNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/most-productive")
    public ResponseEntity<?> getMostProductiveSeller(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime end) {
        if (start.isAfter(end)) {
            throw new InvalidPeriodException("Start date must be before or equal to end date");
        }
        try {
            Seller seller = transactionService.getMostProductiveSeller(start, end);
            return ResponseEntity.ok(seller);
        } catch (RuntimeException e) {
            return ResponseEntity.status(400).body(e.getMessage());
        }
    }

    @GetMapping("/less-than-amount")
    public ResponseEntity<List<Seller>> getSellersWithTotalAmountLessThan(
            @RequestParam double amount,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime end) {
        if (start.isAfter(end)) {
            throw new InvalidPeriodException("Start date must be before or equal to end date");
        }
        List<Seller> sellers = transactionService.getSellersWithTotalAmountLessThan(amount, start, end);
        return ResponseEntity.ok(sellers);
    }

    @GetMapping("/best-period")
    public ResponseEntity<?> getBestPeriod(@RequestParam Long sellerId) {
        try {
            Period period = transactionService.findBestPeriod(sellerId);
            return ResponseEntity.ok(period);
        } catch (SellerNotFoundException e) {
            return ResponseEntity.status(404).body(e.getMessage());
        }
    }
}
package ru.nsu.garkusha.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.nsu.garkusha.dto.Period;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.entities.Transaction;
import ru.nsu.garkusha.exception.SellerNotFoundException;
import ru.nsu.garkusha.repositories.ISellerRepository;
import ru.nsu.garkusha.repositories.ITransactionRepository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class TransactionService {
    private final ITransactionRepository transactionRepository;
    private final ISellerRepository sellerRepository;

    @Autowired
    public TransactionService(ITransactionRepository transactionRepository, ISellerRepository sellerRepository) {
        this.transactionRepository = transactionRepository;
        this.sellerRepository = sellerRepository;
    }

    public List<Transaction> transactionsList() {
        return transactionRepository.findAllActive();
    }

    public Optional<Transaction> transactionById(Long id) {
        return transactionRepository.findActiveById(id);
    }

    public Transaction createTransaction(Transaction transaction) {
        Long sellerId = transaction.getSeller().getId();
        if (!sellerRepository.existsActiveById(sellerId)) {
            throw new SellerNotFoundException("Seller with id " + sellerId + " not found or deleted");
        }
        transaction.setDeleted(false);
        transaction.setDeletedDate(null);
        return transactionRepository.save(transaction);
    }

    public List<Transaction> allSellerTransactions(Long id) {
        if (!sellerRepository.existsActiveById(id)) {
            throw new SellerNotFoundException("Seller with id " + id + " not found or deleted");
        }
        return transactionRepository.findActiveBySellerId(id);
    }

    public Seller getMostProductiveSeller(LocalDateTime start, LocalDateTime end) {
        List<Seller> sellers = transactionRepository.findMostProductiveSellers(start, end);
        if (sellers == null || sellers.isEmpty()) {
            throw new RuntimeException("No active transactions found in the given period");
        }
        return sellers.get(0);
    }


    public List<Seller> getSellersWithTotalAmountLessThan(double amount, LocalDateTime start, LocalDateTime end) {
        return transactionRepository.findSellersWithTotalAmountLessThan(amount, start, end);
    }

    public Period findBestPeriod(Long sellerId) {
        if (!sellerRepository.existsActiveById(sellerId)) {
            throw new SellerNotFoundException("Seller with id " + sellerId + " not found or deleted");
        }
        List<Transaction> transactions = transactionRepository.findActiveBySellerIdOrderByTransactionDateAsc(sellerId);
        if (transactions.isEmpty()) {
            return new Period(null, null, 0);
        }

        int maxCount = 0;
        LocalDateTime bestStart = null;
        LocalDateTime bestEnd = null;

        for (int i = 0; i < transactions.size(); i++) {
            for (int j = i; j < transactions.size(); j++) {
                int count = j - i + 1;
                if (count > maxCount) {
                    maxCount = count;
                    bestStart = transactions.get(i).getTransactionDate();
                    bestEnd = transactions.get(j).getTransactionDate();
                }
            }
        }

        return new Period(bestStart, bestEnd, maxCount);
    }
}
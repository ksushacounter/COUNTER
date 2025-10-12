import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import ru.nsu.garkusha.dto.Period;
import ru.nsu.garkusha.entities.PaymentType;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.entities.Transaction;
import ru.nsu.garkusha.exception.SellerNotFoundException;
import ru.nsu.garkusha.repositories.ISellerRepository;
import ru.nsu.garkusha.repositories.ITransactionRepository;
import ru.nsu.garkusha.services.TransactionService;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TransactionServiceTest {

    @Mock
    private ITransactionRepository transactionRepository;

    @Mock
    private ISellerRepository sellerRepository;

    @InjectMocks
    private TransactionService transactionService;

    private Seller seller;
    private Transaction transaction1;
    private Transaction transaction2;

    @BeforeEach
    void setUp() {
        seller = new Seller("Test Seller", "test@email.com", LocalDateTime.now().minusDays(10));
        seller.setId(1L);

        transaction1 = new Transaction(seller, 100.0, PaymentType.CASH, LocalDateTime.now().minusDays(5));
        transaction1.setId(1L);

        transaction2 = new Transaction(seller, 200.0, PaymentType.CARD, LocalDateTime.now().minusDays(3));
        transaction2.setId(2L);
    }

    @Test
    void transactionsList_shouldReturnAllActiveTransactions() {
        List<Transaction> expected = Arrays.asList(transaction1, transaction2);
        when(transactionRepository.findAllActive()).thenReturn(expected);

        List<Transaction> result = transactionService.transactionsList();

        assertEquals(expected, result);
        verify(transactionRepository).findAllActive();
    }

    @Test
    void transactionById_shouldReturnTransactionWhenExists() {
        when(transactionRepository.findActiveById(1L)).thenReturn(Optional.of(transaction1));

        Optional<Transaction> result = transactionService.transactionById(1L);

        assertTrue(result.isPresent());
        assertEquals(transaction1, result.get());
    }

    @Test
    void transactionById_shouldReturnEmptyWhenNotExists() {
        when(transactionRepository.findActiveById(99L)).thenReturn(Optional.empty());

        Optional<Transaction> result = transactionService.transactionById(99L);

        assertFalse(result.isPresent());
    }

    @Test
    void createTransaction_shouldSaveTransactionWhenSellerExists() {
        when(sellerRepository.existsActiveById(1L)).thenReturn(true);
        when(transactionRepository.save(any(Transaction.class))).thenReturn(transaction1);

        Transaction result = transactionService.createTransaction(transaction1);

        assertEquals(transaction1, result);
        verify(transactionRepository).save(transaction1);
        assertFalse(result.isDeleted());
    }

    @Test
    void createTransaction_shouldThrowExceptionWhenSellerNotExists() {
        when(sellerRepository.existsActiveById(1L)).thenReturn(false);

        assertThrows(SellerNotFoundException.class, () -> transactionService.createTransaction(transaction1));
    }

    @Test
    void allSellerTransactions_shouldReturnTransactionsWhenSellerExists() {
        List<Transaction> expected = Arrays.asList(transaction1, transaction2);
        when(sellerRepository.existsActiveById(1L)).thenReturn(true);
        when(transactionRepository.findActiveBySellerId(1L)).thenReturn(expected);

        List<Transaction> result = transactionService.allSellerTransactions(1L);

        assertEquals(expected, result);
    }

    @Test
    void allSellerTransactions_shouldThrowExceptionWhenSellerNotExists() {
        when(sellerRepository.existsActiveById(99L)).thenReturn(false);

        assertThrows(SellerNotFoundException.class, () -> transactionService.allSellerTransactions(99L));
    }

    @Test
    void getMostProductiveSeller_shouldReturnSellerWhenTransactionsExist() {
        LocalDateTime start = LocalDateTime.now().minusDays(10);
        LocalDateTime end = LocalDateTime.now();

        when(transactionRepository.findMostProductiveSellers(start, end))
                .thenReturn(List.of(seller));

        Seller result = transactionService.getMostProductiveSeller(start, end);

        assertEquals(seller, result);
    }

    @Test
    void getMostProductiveSeller_shouldThrowExceptionWhenNoTransactions() {
        LocalDateTime start = LocalDateTime.now().minusDays(10);
        LocalDateTime end = LocalDateTime.now();

        when(transactionRepository.findMostProductiveSellers(start, end))
                .thenReturn(List.of());

        assertThrows(RuntimeException.class,
                () -> transactionService.getMostProductiveSeller(start, end));
    }


    @Test
    void getSellersWithTotalAmountLessThan_shouldReturnSellers() {
        LocalDateTime start = LocalDateTime.now().minusDays(10);
        LocalDateTime end = LocalDateTime.now();
        List<Seller> expected = Collections.singletonList(seller);
        when(transactionRepository.findSellersWithTotalAmountLessThan(150.0, start, end)).thenReturn(expected);

        List<Seller> result = transactionService.getSellersWithTotalAmountLessThan(150.0, start, end);

        assertEquals(expected, result);
    }

    @Test
    void findBestPeriod_shouldReturnPeriodWhenTransactionsExist() {
        when(sellerRepository.existsActiveById(1L)).thenReturn(true);
        List<Transaction> transactions = Arrays.asList(transaction1, transaction2);
        when(transactionRepository.findActiveBySellerIdOrderByTransactionDateAsc(1L)).thenReturn(transactions);

        Period result = transactionService.findBestPeriod(1L);

        assertEquals(2, result.getCount());
        assertEquals(transaction1.getTransactionDate(), result.getStart());
        assertEquals(transaction2.getTransactionDate(), result.getEnd());
    }

    @Test
    void findBestPeriod_shouldReturnEmptyPeriodWhenNoTransactions() {
        when(sellerRepository.existsActiveById(1L)).thenReturn(true);
        when(transactionRepository.findActiveBySellerIdOrderByTransactionDateAsc(1L)).thenReturn(Collections.emptyList());

        Period result = transactionService.findBestPeriod(1L);

        assertEquals(0, result.getCount());
        assertNull(result.getStart());
        assertNull(result.getEnd());
    }

    @Test
    void findBestPeriod_shouldThrowExceptionWhenSellerNotExists() {
        when(sellerRepository.existsActiveById(99L)).thenReturn(false);

        assertThrows(SellerNotFoundException.class, () -> transactionService.findBestPeriod(99L));
    }
}
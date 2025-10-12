import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import ru.nsu.garkusha.controllers.TransactionController;
import ru.nsu.garkusha.dto.Period;
import ru.nsu.garkusha.entities.PaymentType;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.entities.Transaction;
import ru.nsu.garkusha.exception.SellerNotFoundException;
import ru.nsu.garkusha.services.TransactionService;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TransactionController.class)
@ContextConfiguration(classes = ru.nsu.garkusha.CrmSystemApplication.class)
class TransactionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TransactionService transactionService;

    @Autowired
    private ObjectMapper objectMapper;

    private Transaction transaction;
    private Seller seller;

    @BeforeEach
    void setUp() {
        seller = new Seller("Test Seller", "test@email.com", LocalDateTime.now().minusDays(10));
        seller.setId(1L);

        transaction = new Transaction(seller, 100.0, PaymentType.CASH, LocalDateTime.now().minusDays(5));
        transaction.setId(1L);
    }

    @Test
    void getAllTransactions_shouldReturnList() throws Exception {
        List<Transaction> transactions = Arrays.asList(transaction);
        when(transactionService.transactionsList()).thenReturn(transactions);

        mockMvc.perform(get("/api/transactions"))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(transactions)));
    }

    @Test
    void getTransactionById_shouldReturnTransactionWhenExists() throws Exception {
        when(transactionService.transactionById(1L)).thenReturn(Optional.of(transaction));

        mockMvc.perform(get("/api/transactions/1"))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(transaction)));
    }

    @Test
    void getTransactionById_shouldReturnNotFoundWhenNotExists() throws Exception {
        when(transactionService.transactionById(99L)).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/transactions/99"))
                .andExpect(status().isNotFound());
    }

    @Test
    void createTransaction_shouldCreateWhenValid() throws Exception {
        when(transactionService.createTransaction(any(Transaction.class))).thenReturn(transaction);

        mockMvc.perform(post("/api/transactions")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(transaction)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(transaction)));
    }

    @Test
    void createTransaction_shouldReturnNotFoundWhenSellerNotExists() throws Exception {
        when(transactionService.createTransaction(any(Transaction.class))).thenThrow(new SellerNotFoundException("Not found"));

        mockMvc.perform(post("/api/transactions")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(transaction)))
                .andExpect(status().isNotFound());
    }

    @Test
    void getTransactionsBySellerId_shouldReturnListWhenSellerExists() throws Exception {
        List<Transaction> transactions = Arrays.asList(transaction);
        when(transactionService.allSellerTransactions(1L)).thenReturn(transactions);

        mockMvc.perform(get("/api/transactions/seller/1"))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(transactions)));
    }

    @Test
    void getTransactionsBySellerId_shouldReturnNotFoundWhenSellerNotExists() throws Exception {
        when(transactionService.allSellerTransactions(99L)).thenThrow(new SellerNotFoundException("Not found"));

        mockMvc.perform(get("/api/transactions/seller/99"))
                .andExpect(status().isNotFound());
    }

    @Test
    void getMostProductiveSeller_shouldReturnSellerWhenValid() throws Exception {
        LocalDateTime start = LocalDateTime.now().minusDays(10);
        LocalDateTime end = LocalDateTime.now();
        when(transactionService.getMostProductiveSeller(any(LocalDateTime.class), any(LocalDateTime.class))).thenReturn(seller);

        mockMvc.perform(get("/api/transactions/most-productive")
                        .param("start", start.toString())
                        .param("end", end.toString()))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(seller)));
    }

    @Test
    void getMostProductiveSeller_shouldReturnBadRequestWhenInvalidPeriod() throws Exception {
        LocalDateTime start = LocalDateTime.now();
        LocalDateTime end = LocalDateTime.now().minusDays(10);

        mockMvc.perform(get("/api/transactions/most-productive")
                        .param("start", start.toString())
                        .param("end", end.toString()))
                .andExpect(status().isBadRequest());
    }

    @Test
    void getSellersWithTotalAmountLessThan_shouldReturnListWhenValid() throws Exception {
        LocalDateTime start = LocalDateTime.now().minusDays(10);
        LocalDateTime end = LocalDateTime.now();
        List<Seller> sellers = Arrays.asList(seller);
        when(transactionService.getSellersWithTotalAmountLessThan(anyDouble(), any(LocalDateTime.class), any(LocalDateTime.class))).thenReturn(sellers);

        mockMvc.perform(get("/api/transactions/less-than-amount")
                        .param("amount", "150.0")
                        .param("start", start.toString())
                        .param("end", end.toString()))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(sellers)));
    }

    @Test
    void getSellersWithTotalAmountLessThan_shouldReturnBadRequestWhenInvalidPeriod() throws Exception {
        LocalDateTime start = LocalDateTime.now();
        LocalDateTime end = LocalDateTime.now().minusDays(10);

        mockMvc.perform(get("/api/transactions/less-than-amount")
                        .param("amount", "150.0")
                        .param("start", start.toString())
                        .param("end", end.toString()))
                .andExpect(status().isBadRequest());
    }

    @Test
    void getBestPeriod_shouldReturnPeriodWhenSellerExists() throws Exception {
        Period period = new Period(LocalDateTime.now().minusDays(5), LocalDateTime.now(), 2);
        when(transactionService.findBestPeriod(1L)).thenReturn(period);

        mockMvc.perform(get("/api/transactions/best-period")
                        .param("sellerId", "1"))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(period)));
    }

    @Test
    void getBestPeriod_shouldReturnNotFoundWhenSellerNotExists() throws Exception {
        when(transactionService.findBestPeriod(99L)).thenThrow(new SellerNotFoundException("Not found"));

        mockMvc.perform(get("/api/transactions/best-period")
                        .param("sellerId", "99"))
                .andExpect(status().isNotFound());
    }
}
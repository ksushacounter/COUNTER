import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import ru.nsu.garkusha.controllers.SellerController;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.exception.SellerNotFoundException;
import ru.nsu.garkusha.services.SellerService;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(SellerController.class)
class SellerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SellerService sellerService;

    @Autowired
    private ObjectMapper objectMapper;

    private Seller seller;

    @BeforeEach
    void setUp() {
        seller = new Seller("Test Seller", "test@email.com", LocalDateTime.now().minusDays(10));
        seller.setId(1L);
    }

    @Test
    void getAllSellers_shouldReturnList() throws Exception {
        List<Seller> sellers = Arrays.asList(seller);
        when(sellerService.sellersList()).thenReturn(sellers);

        mockMvc.perform(get("/api/sellers"))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(sellers)));
    }

    @Test
    void getSellerById_shouldReturnSellerWhenExists() throws Exception {
        when(sellerService.sellerById(1L)).thenReturn(Optional.of(seller));

        mockMvc.perform(get("/api/sellers/1"))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(seller)));
    }

    @Test
    void getSellerById_shouldReturnNotFoundWhenNotExists() throws Exception {
        when(sellerService.sellerById(99L)).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/sellers/99"))
                .andExpect(status().isNotFound());
    }

    @Test
    void createSeller_shouldCreateAndReturnSeller() throws Exception {
        when(sellerService.createNewSeller(any(Seller.class))).thenReturn(seller);

        mockMvc.perform(post("/api/sellers")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(seller)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(seller)));
    }

    @Test
    void updateSeller_shouldUpdateWhenExists() throws Exception {
        when(sellerService.updateSeller(anyLong(), any(Seller.class))).thenReturn(seller);

        mockMvc.perform(put("/api/sellers/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(seller)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(seller)));
    }

    @Test
    void updateSeller_shouldReturnNotFoundWhenNotExists() throws Exception {
        when(sellerService.updateSeller(anyLong(), any(Seller.class))).thenThrow(new SellerNotFoundException("Not found"));

        mockMvc.perform(put("/api/sellers/99")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(seller)))
                .andExpect(status().isNotFound());
    }

    @Test
    void deleteSeller_shouldDeleteWhenExists() throws Exception {
        doNothing().when(sellerService).deleteSeller(1L);

        mockMvc.perform(delete("/api/sellers/1"))
                .andExpect(status().isOk());
    }

    @Test
    void deleteSeller_shouldReturnNotFoundWhenNotExists() throws Exception {
        doThrow(new SellerNotFoundException("Not found")).when(sellerService).deleteSeller(99L);

        mockMvc.perform(delete("/api/sellers/99"))
                .andExpect(status().isNotFound());
    }
}
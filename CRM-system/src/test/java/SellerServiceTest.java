import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.exception.SellerNotFoundException;
import ru.nsu.garkusha.repositories.ISellerRepository;
import ru.nsu.garkusha.services.SellerService;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SellerServiceTest {

    @Mock
    private ISellerRepository sellerRepository;

    @InjectMocks
    private SellerService sellerService;

    private Seller seller;

    @BeforeEach
    void setUp() {
        seller = new Seller("Test Seller", "test@email.com", LocalDateTime.now().minusDays(10));
        seller.setId(1L);
    }

    @Test
    void sellersList_shouldReturnAllActiveSellers() {
        List<Seller> expected = Arrays.asList(seller);
        when(sellerRepository.findAllActive()).thenReturn(expected);

        List<Seller> result = sellerService.sellersList();

        assertEquals(expected, result);
        verify(sellerRepository).findAllActive();
    }

    @Test
    void sellerById_shouldReturnSellerWhenExists() {
        when(sellerRepository.findActiveById(1L)).thenReturn(Optional.of(seller));

        Optional<Seller> result = sellerService.sellerById(1L);

        assertTrue(result.isPresent());
        assertEquals(seller, result.get());
    }

    @Test
    void sellerById_shouldReturnEmptyWhenNotExists() {
        when(sellerRepository.findActiveById(99L)).thenReturn(Optional.empty());

        Optional<Seller> result = sellerService.sellerById(99L);

        assertFalse(result.isPresent());
    }

    @Test
    void createNewSeller_shouldSaveSeller() {
        when(sellerRepository.save(any(Seller.class))).thenReturn(seller);

        Seller result = sellerService.createNewSeller(seller);

        assertEquals(seller, result);
        assertFalse(result.isDeleted());
        verify(sellerRepository).save(seller);
    }

    @Test
    void updateSeller_shouldUpdateWhenSellerExists() {
        Seller updatedInfo = new Seller("Updated Name", "updated@email.com", LocalDateTime.now());
        when(sellerRepository.findActiveById(1L)).thenReturn(Optional.of(seller));
        when(sellerRepository.save(any(Seller.class))).thenReturn(seller);

        Seller result = sellerService.updateSeller(1L, updatedInfo);

        assertEquals("Updated Name", result.getName());
        assertEquals("updated@email.com", result.getContactInfo());
        verify(sellerRepository).save(seller);
    }

    @Test
    void updateSeller_shouldThrowExceptionWhenSellerNotExists() {
        when(sellerRepository.findActiveById(99L)).thenReturn(Optional.empty());

        assertThrows(SellerNotFoundException.class, () -> sellerService.updateSeller(99L, seller));
    }

    @Test
    void deleteSeller_shouldSoftDeleteWhenSellerExists() {
        when(sellerRepository.findActiveById(1L)).thenReturn(Optional.of(seller));
        when(sellerRepository.save(any(Seller.class))).thenReturn(seller);

        sellerService.deleteSeller(1L);

        assertTrue(seller.isDeleted());
        assertNotNull(seller.getDeletedDate());
        verify(sellerRepository).save(seller);
    }

    @Test
    void deleteSeller_shouldThrowExceptionWhenSellerNotExists() {
        when(sellerRepository.findActiveById(99L)).thenReturn(Optional.empty());

        assertThrows(SellerNotFoundException.class, () -> sellerService.deleteSeller(99L));
    }
}
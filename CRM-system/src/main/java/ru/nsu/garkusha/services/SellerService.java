package ru.nsu.garkusha.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.repositories.ISellerRepository;
import ru.nsu.garkusha.exception.SellerNotFoundException;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class SellerService {

    private final ISellerRepository sellerRepository;

    @Autowired
    public SellerService(ISellerRepository sellerRepository) {
        this.sellerRepository = sellerRepository;
    }

    public List<Seller> sellersList() {
        return sellerRepository.findAllActive();
    }

    public Optional<Seller> sellerById(Long id) {
        return sellerRepository.findActiveById(id);
    }

    public Seller createNewSeller(Seller seller) {
        seller.setDeleted(false);
        return sellerRepository.save(seller);
    }

    public Seller updateSeller(Long id, Seller sellerInfo) {
        Seller seller = sellerRepository.findActiveById(id)
                .orElseThrow(() -> new SellerNotFoundException("Seller not found with id " + id));
        seller.setName(sellerInfo.getName());
        seller.setContactInfo(sellerInfo.getContactInfo());
        return sellerRepository.save(seller);
    }

    public void deleteSeller(Long id) {
        Seller seller = sellerRepository.findActiveById(id)
                .orElseThrow(() -> new SellerNotFoundException("Seller not found with id " + id));
        seller.setDeleted(true);
        seller.setDeletedDate(LocalDateTime.now());
        sellerRepository.save(seller);
    }
}
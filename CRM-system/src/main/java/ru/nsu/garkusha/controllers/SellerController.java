package ru.nsu.garkusha.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import ru.nsu.garkusha.entities.Seller;
import ru.nsu.garkusha.services.SellerService;
import ru.nsu.garkusha.exception.SellerNotFoundException;

import jakarta.validation.Valid;

import java.util.List;

@RestController
@RequestMapping("/api/sellers")
@Validated
public class SellerController {

    private final SellerService sellerService;

    @Autowired
    public SellerController(SellerService sellerService) {
        this.sellerService = sellerService;
    }

    @GetMapping
    public List<Seller> getAllSellers() {
        return sellerService.sellersList();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Seller> getSellerById(@PathVariable Long id) {
        return sellerService.sellerById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public Seller createSeller(@Valid @RequestBody Seller seller) {
        return sellerService.createNewSeller(seller);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateSeller(@PathVariable Long id, @Valid @RequestBody Seller sellerDetails) {
        try {
            Seller updatedSeller = sellerService.updateSeller(id, sellerDetails);
            return ResponseEntity.ok(updatedSeller);
        } catch (SellerNotFoundException e) {
            return ResponseEntity.status(404).body(e.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteSeller(@PathVariable Long id) {
        try {
            sellerService.deleteSeller(id);
            return ResponseEntity.ok().build();
        } catch (SellerNotFoundException e) {
            return ResponseEntity.status(404).body(e.getMessage());
        }
    }
}